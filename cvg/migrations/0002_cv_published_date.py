# Generated by Django 3.2.6 on 2021-08-19 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cvg', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cv',
            name='published_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]