from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer as BaseUserSerializer

from main.fields import FriendToAddRelatedField, FriendToRemoveRelatedField
from rest_framework import serializers


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
        friend_set = set(instance.get_friend_relations())
        friend_to_add = set(validated_data.pop("friend_to_add"))
        friend_to_remove = set(validated_data.pop("friend_to_remove"))

        friend_set |= friend_to_add
        friend_set -= friend_to_remove

        validated_data["friend_set"] = friend_set
        return super().update(instance, validated_data)

    class Meta:
        model = get_user_model()
        fields = ["friend_to_add", "friend_to_remove"]


class UserSerializer(BaseUserSerializer):
    is_friend_requested = serializers.SerializerMethodField()
    is_friend_accepted = serializers.SerializerMethodField()

    def get_is_friend_requested(self, obj):
        user = self.context["request"].user
        return user.is_friend_requested(obj)

    def get_is_friend_accepted(self, obj):
        user = self.context["request"].user
        return obj.is_friend_requested(user)

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + (
            "is_friend_requested",
            "is_friend_accepted",
        )
