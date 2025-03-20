from django.shortcuts import render, redirect
from workout.models import Exercise, Workouts
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