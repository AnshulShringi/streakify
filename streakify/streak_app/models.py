from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from datetime import datetime


class StreakTypeChoices(models.IntegerChoices):
    Definite = 0
    Indefinite = 1


class Streak(TimeStampedModel):
    type = models.IntegerField(_("Type of Streak"), choices=StreakTypeChoices.choices, default=0)
    name = models.CharField(_("Streak Name"), max_length=100)
    max_duration = models.PositiveIntegerField(_("Maximum Duration in days"), null=True, blank=True)
    start_date = models.DateTimeField(_('Starting From'), default=datetime.utcnow)
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=False, null=False,
                              related_name="user_streak")

    streak_image = models.URLField(_("Streak Image"), max_length=300, blank=True, null=True)

    def __str__(self):
        return self.name


class StreakRecord(TimeStampedModel):
    participant = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=False, null=False,
                              related_name="user_record")
    streak =  models.ForeignKey('streak_app.Streak', on_delete=models.CASCADE, blank=False, null=False,
                              related_name="streak_record")
    start_date = models.DateTimeField(_("Starting From"), null=True, blank=True)
    punch_in = models.BooleanField(default=False)

    def __str__(self):
        return "{}:{}".format(self.streak, self.participant)

    class Meta:
        unique_together = ('streak', 'participant',)
