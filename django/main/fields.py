from django.contrib.auth import get_user_model
from rest_framework.serializers import PrimaryKeyRelatedField


class FriendToAddRelatedField(PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context["request"].user
        return get_user_model().objects.exclude(pk=user.pk)


class FriendToRemoveRelatedField(PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context["request"].user
        return user.get_friend_requests()
