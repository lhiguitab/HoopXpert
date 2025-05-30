# Generated by Django 5.1.6 on 2025-03-20 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workouts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('workout_type', models.CharField(choices=[('Push', 'Push'), ('Pull', 'Pull'), ('Legs/Abs', 'Legs & Abs')], max_length=20)),
                ('exercises', models.ManyToManyField(to='workout.exercise')),
            ],
        ),
    ]
