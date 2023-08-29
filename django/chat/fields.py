from rest_framework.serializers import HiddenField, PrimaryKeyRelatedField

from .models import Room


class UserRoomRelatedField(PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context["request"].user
        return Room.objects.filter_by_user(user)


class RoomMembersToAddRelatedField(PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context["request"].user
        return user.get_friends()


class PresetField(HiddenField):
    def __init__(self, **kwargs):
        assert "default" in kwargs, "default is a required argument."
        super(HiddenField, self).__init__(**kwargs)

    def get_value(self, dictionary):
        return super(HiddenField, self).get_value(dictionary)

    def to_representation(self, value):
        return str(value)
