from celery import shared_task
from streakify.streak_app.models import StreakRecord


@shared_task
def update_punch_in():
    # Update start-date of streakrecord of user where user not punched in 
    StreakRecord.objects.filter(punch_in=False).update(start_date=None)

    # Punch out all users for the next day
    StreakRecord.objects.all().update(punch_in=False)