# Generated by Django 3.2.5 on 2021-08-01 12:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0003_alter_post_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 12, 0, 38, 282634, tzinfo=utc)),
        ),
    ]
