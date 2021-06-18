from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from streakify.users.models import User


class RequestChoices(models.IntegerChoices):
    Pending = 0
    Accepted = 1
    Rejected = 2


class Friend(TimeStampedModel):
    status = models.IntegerField(
        _("Request Status"), choices=RequestChoices.choices, max_length=20, default=0)
    server = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=False, null=False,
                        related_name="friend_server")
    client = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=False, null=False,
                        related_name="friend_client")

    def __str__(self):
        return "{}:{}".format(self.server, self.client)
