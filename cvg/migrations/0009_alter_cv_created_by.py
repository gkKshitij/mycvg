# Generated by Django 3.2.5 on 2021-08-18 03:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cvg', '0008_auto_20210818_0903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cv',
            name='created_by',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
