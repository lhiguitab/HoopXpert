from django.shortcuts import render, redirect
from workout.models import Exercise, Workouts, WorkoutProgress, RoutineImprovement
from django.contrib.auth.models import User
from user.models import player  
from django.contrib import messages
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
    player_id = request.session.get('player_id')
    if not player_id:
        return redirect('/login/')

    workouts = Workouts.objects.all()
    exercises = Exercise.objects.none()  # Por defecto vacío

    selected_workout_id = request.GET.get('workout') or request.POST.get('workout')
    if selected_workout_id:
        try:
            selected_workout = Workouts.objects.get(id=selected_workout_id)
            exercises = selected_workout.exercises.all()
        except Workouts.DoesNotExist:
            selected_workout = None
            exercises = Exercise.objects.none()
    else:
        selected_workout = None

    if request.method == 'POST':
        exercise_id = request.POST.get('exercise')
        reps = request.POST.get('reps')
        sets = request.POST.get('sets')
        weight = request.POST.get('weight')
        notes = request.POST.get('notes', '')

        if not all([selected_workout_id, exercise_id, reps, sets, weight]):
            return render(request, 'track_progress.html', {
                'workouts': workouts,
                'exercises': exercises,
                'error': 'Please fill in all required fields.',
                'prev_workout': selected_workout_id,
                'prev_exercise': exercise_id,
                'prev_reps': reps,
                'prev_sets': sets,
                'prev_weight': weight,
                'prev_notes': notes
            })

        workout = Workouts.objects.get(id=selected_workout_id)
        exercise = Exercise.objects.get(id=exercise_id)
        user = player.objects.get(id=player_id)

        WorkoutProgress.objects.create(
            user=user,
            workout=workout,
            exercise=exercise,
            reps=reps,
            sets=sets,
            weight=weight,
            notes=notes
        )

        from django.contrib import messages
        messages.success(request, "✅ Progress saved successfully!")
        return redirect('/main/')

    return render(request, 'track_progress.html', {
        'workouts': workouts,
        'exercises': exercises,
        'prev_workout': selected_workout_id
    })




def routine_improvement(request):
    workouts = Workouts.objects.all()

    if request.method == 'POST':
        workout_id = request.POST.get('workout')
        minutes_trained = request.POST.get('minutes_trained')
        intensity = request.POST.get('intensity')
        completed_workout = request.POST.get('completed_workout') == 'Yes'
        struggled_exercise = request.POST.get('struggled_exercise', '')
        difficulty_rating = request.POST.get('difficulty_rating')

        workout = Workouts.objects.get(id=workout_id)

        # Recuperar el usuario desde la sesión
        player_id = request.session.get('player_id')
        if not player_id:
            return redirect('/login/')

        from user.models import player
        user_instance = player.objects.get(id=player_id)

        # Guardar en base de datos
        RoutineImprovement.objects.create(
            user=user_instance,
            workout=workout,
            minutes_trained=minutes_trained,
            intensity=intensity,
            completed_workout=completed_workout,
            struggled_exercise=struggled_exercise,
            difficulty_rating=difficulty_rating
        )

        # Este mensaje se mostrará en el home
        messages.success(request, '✅ Routine improvement data saved successfully!')
       
        # Redirigir al home una vez guardado
        return redirect('/main/')

    return render(request, 'routine_improvement.html', {'workouts': workouts})
