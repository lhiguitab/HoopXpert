from django.db import models
from django.contrib.auth.models import User

class Exercise(models.Model):
    exercise_name = models.CharField(max_length=100)
    short_youtube_demonstration = models.URLField(max_length=500, blank=True)
    in_depth_youtube_explanation = models.URLField(max_length=500, blank=True)
    difficulty_level = models.CharField(max_length=50)
    target_muscle_group = models.CharField(max_length=100)
    prime_mover_muscle = models.CharField(max_length=100, blank=True)
    secondary_muscle = models.CharField(max_length=100, blank=True)
    tertiary_muscle = models.CharField(max_length=100, blank=True)
    primary_equipment = models.CharField(max_length=100)
    primary_items = models.PositiveIntegerField(default=0)
    secondary_equipment = models.CharField(max_length=100, blank=True)
    secondary_items = models.PositiveIntegerField(default=0)
    posture = models.CharField(max_length=50)
    single_or_double_arm = models.CharField(max_length=50)
    continuous_or_alternating_arms = models.CharField(max_length=50)
    grip = models.CharField(max_length=50)
    load_position_ending = models.CharField(max_length=100, blank=True)
    continuous_or_alternating_legs = models.CharField(max_length=50)
    foot_elevation = models.CharField(max_length=50)
    combination_exercises = models.CharField(max_length=100)
    movement_pattern_1 = models.CharField(max_length=100)
    movement_pattern_2 = models.CharField(max_length=100, blank=True)
    movement_pattern_3 = models.CharField(max_length=100, blank=True)
    plane_of_motion_1 = models.CharField(max_length=50)
    plane_of_motion_2 = models.CharField(max_length=50, blank=True)
    plane_of_motion_3 = models.CharField(max_length=50, blank=True)
    body_region = models.CharField(max_length=50)
    force_type = models.CharField(max_length=50)
    mechanics = models.CharField(max_length=50)
    laterality = models.CharField(max_length=50)
    primary_exercise_classification = models.CharField(max_length=100)

    def __str__(self):
        return self.exercise_name
    
class Workouts(models.Model):
    WORKOUT_TYPES = [
        ('Push', 'Push'),
        ('Pull', 'Pull'),
        ('Legs/Abs', 'Legs & Abs'),
    ]

    name = models.CharField(max_length=100)  # Puedes generar un nombre tipo "Push Workout 1"
    workout_type = models.CharField(max_length=20, choices=WORKOUT_TYPES)
    exercises = models.ManyToManyField(Exercise)

    def __str__(self):
        return f"{self.name} - {self.workout_type}"

class WorkoutProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workouts, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight = models.FloatField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.exercise.exercise_name} - {self.date}"    
    
class RoutineImprovement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workouts, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    minutes_trained = models.PositiveIntegerField()
    intensity = models.CharField(max_length=10, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    completed_workout = models.BooleanField()
    struggled_exercise = models.CharField(max_length=100, blank=True, null=True)
    difficulty_rating = models.CharField(max_length=20, choices=[('Too easy', 'Too easy'), ('Just right', 'Just right'), ('Too difficult', 'Too difficult')])

    def __str__(self):
        return f"{self.user.username} - {self.workout.name} - {self.date}"
# Create your models here.
