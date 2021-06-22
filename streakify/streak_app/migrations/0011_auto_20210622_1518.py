# Generated by Django 3.1.11 on 2021-06-22 09:48

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('streak_app', '0010_auto_20210620_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streak',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_streak', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='streak',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 22, 15, 18, 42, 221696), verbose_name='Starting From'),
        ),
        migrations.AlterField(
            model_name='streakrecord',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_record', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='streakrecord',
            name='streak',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='streak_record', to='streak_app.streak'),
        ),
    ]