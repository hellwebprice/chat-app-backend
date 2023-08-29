from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "status", "avatar"]

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

    def get_friend_requests(self):
        return self.friend_set.all()

    def __str__(self):
        return self.username
