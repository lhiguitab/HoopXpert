# Generated by Django 5.1.6 on 2025-05-14 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0011_rename_name_recoveryexercise_exercise_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recoveryplan',
            name='user',
        ),
        migrations.AddField(
            model_name='recoveryplan',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
