from django.contrib.auth import get_user_model

from main.fields import FriendToAddRelatedField, FriendToRemoveRelatedField
from rest_framework import serializers


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "avatar"]


class FriendListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "avatar"]


class FriendUpdateSerializer(serializers.ModelSerializer):
    friend_to_add = FriendToAddRelatedField(
        queryset=get_user_model().objects.all(),
        many=True,
        write_only=True,
        default=[],
    )
    friend_to_remove = FriendToRemoveRelatedField(
        many=True,
        write_only=True,
        default=[],
    )

    def update(self, instance, validated_data):
        friend_set = set(instance.get_friend_requests())
        friend_to_add = set(validated_data.pop("friend_to_add"))
        friend_to_remove = set(validated_data.pop("friend_to_remove"))

        friend_set |= friend_to_add
        friend_set -= friend_to_remove

        validated_data["friend_set"] = friend_set
        return super().update(instance, validated_data)

    class Meta:
        model = get_user_model()
        fields = ["friend_to_add", "friend_to_remove"]
