import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils.translation import gettext_lazy as _

from .managers import MessageManager, RoomManager


class Room(models.Model):
    objects = RoomManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member_set = models.ManyToManyField(
        get_user_model(), verbose_name=_("Room members")
    )
    title = models.CharField(_("Title"), max_length=191, default="Беседа")
    avatar = models.ImageField(
        _("Avatar"), null=True, upload_to="room_avatar/%Y-%m-%d-%H-%M-%S/"
    )

    def __str__(self):
        return str(self.id)

    def get_members(self):
        return self.member_set.all()

    def get_last_message_time(self):
        messages = self.message_set.order_by("-created_at")
        try:
            message = messages[0]
        except IndexError:
            return None
        return message.created_at

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")


class Message(models.Model):
    objects = MessageManager()

    room = models.ForeignKey(Room, models.CASCADE, verbose_name=_("Room"))
    author = models.ForeignKey(
        get_user_model(), models.CASCADE, verbose_name=_("Author")
    )
    text = models.TextField(_("Message text"))
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {truncatechars(self.text, 15)}"

    def is_owner(self, user):
        return self.author == user

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
