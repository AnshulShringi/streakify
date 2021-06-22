from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from streakify.streak_app.models import Streak, StreakRecord
import inspect


@receiver(post_save, sender=Streak)
def owner_streak_record_create_trigger(sender, instance, created, *args, **kwargs):
    request = None
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            break
    if created:
        record = StreakRecord.objects.create(streak=instance, participant=instance.created_by)
        record.save()


post_save.connect(owner_streak_record_create_trigger, sender=Streak)