# Generated by Django 3.1.11 on 2021-06-18 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0002_auto_20210617_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='status',
            field=models.CharField(choices=[(0, 'Pending'), (1, 'Accepted'), (2, 'Rejected')], default=0, max_length=20, verbose_name='Request Status'),
        ),
    ]
