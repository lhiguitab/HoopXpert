# Generated by Django 5.1.6 on 2025-04-24 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0005_alter_routineimprovement_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BasketballDrill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise_name', models.CharField(max_length=100)),
                ('position', models.CharField(choices=[('Point Guard', 'Point Guard'), ('Shooting Guard', 'Shooting Guard'), ('Small Forward', 'Small Forward'), ('Power Forward', 'Power Forward'), ('Center', 'Center'), ('All', 'All Positions')], max_length=50)),
                ('focus_skill', models.CharField(max_length=100)),
                ('duration_min', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='BasketballWorkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('workout_type', models.CharField(max_length=50)),
                ('exercises', models.ManyToManyField(to='workout.basketballdrill')),
            ],
        ),
    ]
