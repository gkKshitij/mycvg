# Generated by Django 3.2.5 on 2021-08-18 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cvg', '0010_alter_cv_first_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cv',
            name='first_name',
            field=models.CharField(max_length=20),
        ),
    ]
