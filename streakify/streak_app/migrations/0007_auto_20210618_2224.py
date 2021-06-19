# Generated by Django 3.1.11 on 2021-06-18 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('streak_app', '0006_auto_20210618_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streak',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='streak_user', to='users.user'),
        ),
    ]