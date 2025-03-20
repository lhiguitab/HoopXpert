from django.contrib import admin
from .models import Exercise, Workouts

# Register your models here.
admin.site.register(Exercise)
@admin.register(Workouts)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'workout_type')
    readonly_fields = ('exercises_list',)

    def exercises_list(self, obj):
        return ", ".join([exercise.exercise_name for exercise in obj.exercises.all()])