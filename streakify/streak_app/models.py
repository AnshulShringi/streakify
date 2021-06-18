from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from datetime import date


class StreakTypeChoices(models.IntegerChoices):
    Definite = 0
    Indefinite = 1


class Streak(TimeStampedModel):
    streak_type = models.IntegerField(
        _("Type of Streak"), choices=StreakTypeChoices.choices, default=0)
    name = models.CharField(_("Streak Name"), max_length=100)
    max_duration = models.PositiveIntegerField(_("Maximum Duration in days"), null=True, blank=True)
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=True, null=True,
                              related_name="streak_user")

    def __str__(self):
        return self.name


class StreakRecord(TimeStampedModel):
    participant = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=False, null=False,
                              related_name="streak_participant")
    streak =  models.ForeignKey('streak_app.Streak', on_delete=models.CASCADE, blank=False, null=False,
                              related_name="streak")
    start_date = models.DateField(_("User started from"), default=date.today)
    punch_in = models.BooleanField(default=False)

    def __str__(self):
        return "{}:{}".format(self.streak, self.participant)

    class Meta:
        unique_together = ('streak', 'participant',)