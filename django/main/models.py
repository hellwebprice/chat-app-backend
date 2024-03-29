from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "status", "avatar"]

    username = models.CharField(_("username"), max_length=150)
    email = models.EmailField(_("email address"), unique=True)
    status = models.CharField(_("Status"), max_length=191, blank=True, null=True)
    avatar = models.ImageField(
        _("Avatar"), null=True, upload_to="avatar/%Y-%m-%d-%H-%M-%S/"
    )
    friend_set = models.ManyToManyField(
        "self", verbose_name=_("Friends"), symmetrical=False
    )

    def get_friends(self):
        return self.friend_set.filter(friend_set=self)

    def get_friend_relations(self):
        return self.friend_set.all()

    def get_friend_requests(self):
        return User.objects.filter(friend_set=self).exclude(
            pk__in=self.friend_set.all()
        )

    def is_friend_requested(self, user):
        return self.friend_set.contains(user)

    def __str__(self):
        return self.username
