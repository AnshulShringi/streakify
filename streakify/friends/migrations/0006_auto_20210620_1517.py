# Generated by Django 3.1.11 on 2021-06-20 09:47

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('friends', '0005_auto_20210618_2224'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='friend',
            unique_together={('server', 'client')},
        ),
    ]