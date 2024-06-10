import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, VerificationCodes
from .serializers import UserSerializer, UserRegistrationSerializer, ProfileUpdateSerializer
from .utils import generate_verification_code, send_welcome_email


class UserManagement(APIView):
    @swagger_auto_schema(operation_description="Get all users or a specific user")
    def get(self, request, username=None):
        if username:
            try:
                user = User.objects.get(username=username)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)

    @swagger_auto_schema(
        request_body=UserSerializer, operation_description="Create a new user"
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            try:
                user = User.objects.get(username=serializer.data["username"])
                send_welcome_email(user)
            except Exception as e:
                print(e)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=UserSerializer, operation_description="Update a user"
    )
    def put(self, request, username):
        try:
            user = User.objects.get(username=username)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Delete a user",
        responses={204: "No Content"},
        properties={
            "username": openapi.Schema(
                type=openapi.TYPE_STRING, description="Username of the user to delete"
            )
        },
    )
    def delete(self, request, username):
        try:
            user = User.objects.get(username=username)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


def login_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("voting:home")

    if request.method == "POST":
        # Extracting data from the query dictionary
        data = request.body.decode("utf-8")
        data = json.loads(data)
        password = data.get("password", None)
        username = data.get("username", None)

        if not username or not password:
            return JsonResponse(
                {"error": "Username and password are required", "status": "failed",
                 "message": "Username and password are required"
                 },

            )
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse(
                {"message": "User logged in successfully", "status": "success"},
                status=status.HTTP_200_OK,
            )
        return JsonResponse(
            {"error": "Invalid username or password", "status": "failed",

             "message": "Invalid username or password"},

        )

    elif request.method == "GET":
        return render(request, "system/signin.html")


def logout_view(request: HttpRequest):
    logout(request)
    return JsonResponse(
        status=status.HTTP_200_OK,
        data={
            "message": "User logged out successfully",
            "status": "success",
        },
    )


@login_required(login_url="/accounts/login/")
@api_view(["GET", "POST"])
def profile(request):
    if request.method == "GET":
        user = request.user
        return render(request, "accounts/profile.html", {"user": user})

    elif request.method == "POST":
        serializer = ProfileUpdateSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={"message": "Profile updated successfully", "status": "success"},
                status=status.HTTP_200_OK,
            )
        return Response(
            data={"message": "Profile update failed", "status": "failed"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class VerificationCodesView(APIView):
    @swagger_auto_schema(
        operation_description="Generate a verification code for the authenticated user"
    )
    def post(self, request):
        if request.user.is_authenticated:
            random_code = generate_verification_code()
            user = request.user
            subject = "Go-Vote Email Verification"
            html_content = render_to_string(
                "accounts/verification_email.html", {"verification_code": random_code}
            )
            email = EmailMessage(
                subject, html_content, "no-reply@go-vote.com", [user.email]
            )
            email.content_subtype = "html"
            email.send()
            VerificationCodes.objects.create(user=user, code=random_code).save()

            # send the code to the user

            return Response(data={"status": "success"}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(
        operation_description="Verify the user-supplied code for the authenticated user",
        manual_parameters=[
            openapi.Parameter(
                name="code",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="Verification code",
            )
        ],
    )
    def get(self, request):

        if request.user.is_authenticated:
            user = request.user
            user_supplied_code = request.GET.get("code", None)
            try:
                verification_code = VerificationCodes.objects.get(user=user)
                if verification_code.code == user_supplied_code:
                    verification_code.is_used = True
                    verification_code.user.email_verified = True
                    verification_code.user.save()
                    verification_code.save()
                    # delete the code
                    verification_code.delete()
                    return Response(
                        data={"message": "Code verified", "status": "success"},
                        status=status.HTTP_200_OK,
                    )
                return Response(
                    data={"message": "Code does not match", "status": "failed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except VerificationCodes.DoesNotExist:
                return Response(
                    data={"message": "No verification code found", "status": "failed"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@login_required(login_url="/accounts/login/")
def email_verification_page(request: HttpRequest):
    return render(request, "accounts/verify.html")


@api_view(['POST', 'GET'])
def register_user(request):
    # logout the user if they are already logged in
    if request.user.is_authenticated:
        logout(request)
    if request.method == 'POST':

        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully", "status": "success"},
                            status=status.HTTP_201_CREATED)

        return Response({
            "errors": serializer.errors,
            "status": "failed",
        }, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        return render(request, 'system/register.html')
