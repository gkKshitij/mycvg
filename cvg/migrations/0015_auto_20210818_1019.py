# Generated by Django 3.2.5 on 2021-08-18 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cvg', '0014_alter_cv_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cv',
            name='address',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='cv',
            name='age',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='cv',
            name='college_email_id',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='cv',
            name='mobile_number',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='cv',
            name='personal_email_id',
            field=models.CharField(max_length=30),
        ),
    ]
