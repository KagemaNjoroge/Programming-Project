from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Poll, PollInvitation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email"]  # Add other fields if needed


class PollSerializer(serializers.ModelSerializer):
    candidates = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(), many=True, required=False
    )

    class Meta:
        model = Poll
        fields = [
            "id",
            "title",
            "description",
            "start_date",
            "end_date",
            "created_by",
            "avatar",
        ]


class PollInvitationSerializer(serializers.ModelSerializer):

    class Meta:
        model = PollInvitation
        fields = "__all__"
