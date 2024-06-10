from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.utils.translation import gettext_lazy as _
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'phone_number', 'profile_image', 'role', 'address']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already taken.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already taken.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number', ''),
            profile_image=validated_data.get('profile_image', 'profile/default/avatar.png'),
            role=validated_data.get('role', 'voter'),
            address=validated_data.get('address', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    password = serializers.CharField(write_only=True, required=False)

    def create(self, validated_data):
        password = validated_data.pop("password", None)

        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.vote_balance = 0
        instance.save()
        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        ret.pop("is_superuser", None)
        ret.pop("is_staff", None)
        ret.pop("is_active", None)
        ret.pop("date_joined", None)
        ret.pop("last_login", None)
        ret.pop("groups", None)
        return ret


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'profile_image', 'address']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance
