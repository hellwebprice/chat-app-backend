from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from djoser.serializers import UserSerializer
from rest_framework import serializers

from .fields import PresetField, RoomMembersToAddRelatedField, UserRoomRelatedField
from .models import Message, Room


class MessageListSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    is_owner = serializers.SerializerMethodField(
        "view_is_owner", label=_("Is user message owner")
    )

    def view_is_owner(self, instance):
        user = self.context["request"].user
        return instance.is_owner(user)

    class Meta:
        model = Message
        fields = ["author", "is_owner", "text", "created_at"]


class MessageCreateSerializer(serializers.ModelSerializer):
    author = PresetField(default=serializers.CurrentUserDefault())
    room = UserRoomRelatedField(write_only=True)
    is_owner = serializers.SerializerMethodField(
        "view_is_owner", label=_("Is user message owner")
    )

    def view_is_owner(self, instance):
        user = self.context["request"].user
        return instance.is_owner(user)

    def create(self, validated_data):
        instance = super().create(validated_data)
        return instance

    class Meta:
        model = Message
        fields = ["author", "room", "text", "created_at", "is_owner"]
        read_only_fields = ["created_at"]


class RoomListSerializer(serializers.ModelSerializer):
    last_message = MessageListSerializer(source="get_last_message")

    class Meta:
        model = Room
        fields = ["id", "title", "last_message"]


class RoomCreateSerializer(serializers.ModelSerializer):
    member_set = RoomMembersToAddRelatedField(
        many=True,
        write_only=True,
        default=[],
    )

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["member_set"].append(user)
        return super().create(validated_data)

    class Meta:
        model = Room
        fields = ["id", "member_set", "avatar", "title"]


class RoomUpdateSerializer(RoomCreateSerializer):
    member_to_add = RoomMembersToAddRelatedField(
        many=True,
        write_only=True,
        default=[],
    )
    member_to_remove = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        many=True,
        write_only=True,
        default=[],
    )
    member_set = serializers.StringRelatedField(
        many=True,
        label=_("List of room member usernames"),
        read_only=True,
    )

    def update(self, instance, validated_data):
        member_set = set(instance.get_members())
        member_to_add = set(validated_data.pop("member_to_add"))
        member_to_remove = set(validated_data.pop("member_to_remove"))

        member_set |= member_to_add
        member_set -= member_to_remove

        validated_data["member_set"] = member_set
        return super().update(instance, validated_data)

    class Meta:
        model = Room
        fields = ["member_set", "member_to_add", "member_to_remove", "avatar", "title"]


class RoomRetrieveSerializer(serializers.ModelSerializer):
    member_set = serializers.StringRelatedField(
        many=True, label=_("List of room member usernames")
    )

    class Meta:
        model = Room
        fields = ["member_set", "title", "avatar"]
