# Generated by Django 3.2.5 on 2021-08-17 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cvg', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cv',
            old_name='author',
            new_name='sapid',
        ),
        migrations.RemoveField(
            model_name='cv',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='cv',
            name='text',
        ),
        migrations.RemoveField(
            model_name='cv',
            name='title',
        ),
        migrations.AddField(
            model_name='cv',
            name='age',
            field=models.IntegerField(blank=True, default=17, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cv',
            name='cemailid',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='cv',
            name='firstname',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='cv',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Bisesual', 'Bisesual'), ('None', 'None')], default='None', max_length=10),
        ),
        migrations.AddField(
            model_name='cv',
            name='gitprofurl',
            field=models.URLField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='cv',
            name='keywords',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='cv',
            name='lastname',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='cv',
            name='linkedinprofurl',
            field=models.URLField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='cv',
            name='mobilenumber',
            field=models.IntegerField(blank=True, default=9999999999, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cv',
            name='pemailid',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='cv',
            name='address',
            field=models.TextField(blank=True, max_length=100),
        ),
    ]
