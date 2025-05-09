# Generated by Django 5.1.6 on 2025-03-20 07:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0003_workoutprogress'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RoutineImprovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('minutes_trained', models.PositiveIntegerField()),
                ('intensity', models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], max_length=10)),
                ('completed_workout', models.BooleanField()),
                ('struggled_exercise', models.CharField(blank=True, max_length=100, null=True)),
                ('difficulty_rating', models.CharField(choices=[('Too easy', 'Too easy'), ('Just right', 'Just right'), ('Too difficult', 'Too difficult')], max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('workout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workout.workouts')),
            ],
        ),
    ]
