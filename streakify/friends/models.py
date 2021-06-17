from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from streakify.users.models import User


class Friend(TimeStampedModel):
    STATUS_TYPES = (
        ("pending", "pending"),
        ("accepted", "accepted"),
        ("rejected", "rejected"),
    )
    status = models.CharField(
        _("Request Status"), choices=STATUS_TYPES, max_length=20)
    server = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=False, null=False,
                        related_name="friend_server")
    client = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=False, null=False,
                        related_name="friend_client")

    def __str__(self):
        return "{}:{}".format(self.server, self.client)
