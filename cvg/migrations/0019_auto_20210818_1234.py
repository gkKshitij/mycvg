# Generated by Django 3.2.5 on 2021-08-18 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cvg', '0018_academics_extracurricular_internships_projects_roles_skills'),
    ]

    operations = [
        migrations.RenameField(
            model_name='academics',
            old_name='admissionyear',
            new_name='admission_year',
        ),
        migrations.RenameField(
            model_name='academics',
            old_name='graduationyear',
            new_name='graduation_year',
        ),
        migrations.RenameField(
            model_name='academics',
            old_name='tenthpercentile',
            new_name='tenth_percentile',
        ),
        migrations.RenameField(
            model_name='academics',
            old_name='twelvthpercentile',
            new_name='twelvth_percentile',
        ),
    ]
