from rest_framework.serializers import HyperlinkedModelSerializer
from .models import Poll


class PollSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Poll
        fields = "__all__"
