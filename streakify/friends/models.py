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
        _("Request Status"), choices=RequestChoices.choices, default=0)
    server = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=False, null=False,
                        related_name="user_friendserver")
    client = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=False, null=False,
                        related_name="user_friendclient")

    def __str__(self):
        return "{}:{}".format(self.server, self.client)

    class Meta:
        unique_together = ('server', 'client')