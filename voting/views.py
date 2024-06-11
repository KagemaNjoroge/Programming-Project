from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404, render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from blockchain.blockchain import VoteBlockChain
from voting.utils import allocate_votes
from .models import Poll, PollWallet, PollInvitation
from .serializers import PollSerializer, PollInvitationSerializer

vote_blockchain = VoteBlockChain()


@swagger_auto_schema(
    method="get",
    operation_description="Mine pending transactions",
)
@login_required(login_url="/accounts/login/")
@api_view(["GET"])
def mine_transactions(request):
    vote_blockchain.mine_pending_transactions()
    return JsonResponse({"message": "Pending transactions mined."})


@swagger_auto_schema(
    method="post",
    operation_description="Allocate votes to users in a poll",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "votes_{user_id}": openapi.Schema(
                type=openapi.TYPE_INTEGER, description="Number of votes for user"
            )
        },
    ),
)
@api_view(["POST"])
def allocate_votes_view(request, poll_id):
    allocations = {}
    for key, value in request.data.items():
        if key.startswith("votes_"):
            user_id = int(key.split("_")[1])
            votes = int(value)
            allocations[user_id] = votes

    allocate_votes(poll_id, allocations)
    return Response(
        {
            "message": "Votes allocated successfully.",
            "allocations": allocations,
            "poll_id": poll_id,
            "poll_title": Poll.objects.get(id=poll_id).title,
        }
    )


@login_required(login_url="/accounts/login/")
def voting_template_view(request: HttpRequest, poll_id: int):
    # wallets where the user is the current user and poll id = poll_id
    poll = get_object_or_404(Poll, id=poll_id)
    wallet = PollWallet.objects.filter(user=request.user, poll=poll).first()

    return render(request, "voting/voting.html", {"wallet": wallet})


@login_required(login_url="/accounts/login/")
def home(request: HttpRequest):
    return render(request, "system/index.html")


@login_required(login_url="/accounts/login/")
def create_new_poll_page(request: HttpRequest):
    return render(request, "voting/new_poll.html")


class PollListView(LoginRequiredMixin, APIView):
    def get(self, request):
        polls = Poll.objects.all()
        serializer = PollSerializer(polls, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PollSerializer(data=request.data)
        serializer.initial_data["created_by"] = request.user.id

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PollInvitationsView(LoginRequiredMixin, APIView):
    def get(self, request, id: int):
        poll_invitation = get_object_or_404(PollInvitation, id=id)
        serializer = PollInvitationSerializer(poll_invitation, many=False)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new poll invitation",
    )
    def post(self, request):
        serializer = PollInvitationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url="/accounts/login/")
def my_polls_template_view(request: HttpRequest):
    polls = Poll.objects.filter(created_by=request.user)
    return render(request, "voting/my_polls.html", {"polls": polls})


@login_required(login_url="/accounts/login/")
@api_view(["GET"])
def poll_invites_template_view(request: HttpRequest):
    invitations = PollInvitation.objects.filter(invited_user=request.user.email)
    return render(request, "voting/poll_invites.html", {"invitations": invitations})


@login_required(login_url="/accounts/login/")
def invite_users_for_poll(request: HttpRequest, poll_id: int):
    poll = get_object_or_404(Poll, id=poll_id)
    # all users except the current user
    users = get_user_model().objects.exclude(id=request.user.id)

    return render(request, "voting/invite_users.html", {"poll": poll, "users": users})
