from django.db import models


class RoomManager(models.Manager):
    def filter_by_user(self, user):
        return self.get_queryset().filter(member_set=user)


class MessageManager(models.Manager):
    def accessed_by_user(self, user):
        return self.get_queryset().filter(room__member_set=user)
