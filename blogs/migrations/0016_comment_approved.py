# Generated by Django 3.2.5 on 2021-08-04 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0015_alter_comment_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
