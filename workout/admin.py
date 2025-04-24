from django.contrib import admin
from .models import Exercise, Workouts, WorkoutProgress, BasketballDrill, BasketballWorkout, RealGameDrill

# Register your models here.
admin.site.register(Exercise)
@admin.register(Workouts)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'workout_type')
    readonly_fields = ('exercises_list',)

    def exercises_list(self, obj):
        return ", ".join([exercise.exercise_name for exercise in obj.exercises.all()])
admin.site.register(WorkoutProgress)

@admin.register(BasketballDrill)
class BasketballDrillAdmin(admin.ModelAdmin):
    list_display = ('exercise_name', 'position', 'focus_skill', 'duration_min')
    search_fields = ('exercise_name', 'position')

@admin.register(BasketballWorkout)
class BasketballWorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'workout_type')
    filter_horizontal = ('exercises',)

@admin.register(RealGameDrill)
class RealGameDrillAdmin(admin.ModelAdmin):
    list_display = ('title', 'situation_type', 'duration_min')
    search_fields = ('title', 'situation_type')
