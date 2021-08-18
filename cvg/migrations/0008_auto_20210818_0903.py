# Generated by Django 3.2.5 on 2021-08-18 03:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cvg', '0007_alter_cv_sap_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cv',
            name='created_by',
            field=models.ForeignKey(default=9, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cv',
            name='sap_id',
            field=models.IntegerField(blank=True),
        ),
    ]
