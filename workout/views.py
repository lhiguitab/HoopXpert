from django.shortcuts import render, redirect
from workout.models import Exercise, Workouts, WorkoutProgress, RoutineImprovement
from django.contrib.auth.models import User
import random

# Create your views here.
def main(request):
    # Revisar si el player está logueado
    if 'player_id' not in request.session:
        return redirect('/login/')  # Si no hay sesión, redirige al login
    
    # Si el usuario está logueado, muestra la página normal
    return render(request, 'main.html', {'username': request.session.get('username')}) # Por si quieres mostrarlo en el HTML

def exercise(request):
    if request.method == 'POST':
        workout_type = request.POST.get('workout_type')
        workout_exercises = []

        if workout_type:
            if workout_type == 'Push':
                muscle_groups = ['Chest', 'Shoulders', 'Triceps']
            elif workout_type == 'Pull':
                muscle_groups = ['Back', 'Biceps', 'Forearms', 'Trapezius']
            elif workout_type == 'LegsAbs':
                muscle_groups = [
                    'Quadriceps', 'Hamstrings', 'Glutes', 'Adductors',
                    'Abductors', 'Calves', 'Shins', 'Hip Flexors', 'Abdominals'
                ]
            else:
                muscle_groups = []

            if muscle_groups:
                exercises_qs = Exercise.objects.filter(target_muscle_group__in=muscle_groups)

                exercises_list = list(exercises_qs)

                if exercises_list:
                    num_exercises = random.randint(6, 8)
                    selected_exercises = random.sample(exercises_list, min(num_exercises, len(exercises_list)))

                    # Creamos el workout
                    workout_name = f"{workout_type} Workout {Workouts.objects.filter(workout_type=workout_type).count() + 1}"
                    workout = Workouts.objects.create(
                        name=workout_name,
                        workout_type=workout_type
                    )

                    # Asignamos solo los ejercicios seleccionados
                    workout.exercises.set(selected_exercises)

                    workout_exercises = selected_exercises

        context = {
            'workout_type': workout_type,
            'workout_exercises': workout_exercises,
        }
        return render(request, 'workout_generation.html', context)

    return render(request, 'workout_generation.html')

def workout_list(request):
    workouts = Workouts.objects.all()
    return render(request, 'workout_list.html', {'workouts': workouts})

def track_progress(request):
    if request.method == 'POST':
        workout_id = request.POST.get('workout')
        exercise_id = request.POST.get('exercise')
        sets = request.POST.get('sets')
        reps = request.POST.get('reps')
        weight = request.POST.get('weight')
        notes = request.POST.get('notes', '')

        workout = Workouts.objects.get(id=workout_id)
        exercise = Exercise.objects.get(id=exercise_id)

        WorkoutProgress.objects.create(
            user=request.user,
            workout=workout,
            exercise=exercise,
            sets=sets,
            reps=reps,
            weight=weight,
            notes=notes
        )

        return redirect('track_progress')

    workouts = Workouts.objects.all()
    exercises = Exercise.objects.all()
    return render(request, 'track_progress.html', {'workouts': workouts, 'exercises': exercises})

def routine_improvement(request):
    if request.method == 'POST':
        workout_id = request.POST.get('workout')
        minutes_trained = request.POST.get('minutes_trained')
        intensity = request.POST.get('intensity')
        completed_workout = request.POST.get('completed_workout') == 'Yes'
        struggled_exercise = request.POST.get('struggled_exercise', '')
        difficulty_rating = request.POST.get('difficulty_rating')

        workout = Workouts.objects.get(id=workout_id)

        RoutineImprovement.objects.create(
            user=request.user,
            workout=workout,
            minutes_trained=minutes_trained,
            intensity=intensity,
            completed_workout=completed_workout,
            struggled_exercise=struggled_exercise,
            difficulty_rating=difficulty_rating
        )

        return redirect('routine_improvement')

    workouts = Workouts.objects.all()
    return render(request, 'routine_improvement.html', {'workouts': workouts})