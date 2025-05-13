from django.shortcuts import render, redirect
from workout.models import Exercise, Workouts, WorkoutProgress, RoutineImprovement, BasketballDrill, BasketballWorkout, RealGameDrill, RealGameDrillWorkout
from django.contrib.auth.models import User
from user.models import player  
from django.contrib import messages
import random
from datetime import date, datetime, timedelta
from django.db.models import Avg, Max, Count
import calendar

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

def basketball_drills(request):
    if request.method == 'POST':
        selected_position = request.POST.get('position')
        workout_exercises = []

        if selected_position:
            # Filtra drills según la posición seleccionada
            drills_qs = BasketballDrill.objects.filter(position__in=[selected_position, 'All'])
            drills_list = list(drills_qs)

            if drills_list:
                num_exercises = random.randint(3, 4)
                selected_drills = random.sample(drills_list, min(num_exercises, len(drills_list)))

                # Crear un nombre dinámico para la rutina
                workout_name = f"{selected_position} Drill Routine {BasketballWorkout.objects.filter(workout_type=selected_position).count() + 1}"
                workout = BasketballWorkout.objects.create(
                    name=workout_name,
                    workout_type=selected_position
                )

                workout.exercises.set(selected_drills)
                workout_exercises = selected_drills

        context = {
            'position': selected_position,
            'workout_exercises': workout_exercises,
        }
        return render(request, 'drills_generation.html', context)

    return render(request, 'drills_generation.html')

def drills_list(request):
    drills = BasketballWorkout.objects.all()
    return render(request, 'drills_list.html', {'drills': drills})

def real_game_drills(request):
    if request.method == 'POST':
        selected_situation = request.POST.get('scenario')  # 'scenario' es el name del <select>
        workout_exercises = []

        if selected_situation:
            drills_qs = RealGameDrill.objects.filter(situation_type__icontains=selected_situation)
            drills_list = list(drills_qs)

            if drills_list:
                selected_drills = random.sample(drills_list, min(4, len(drills_list)))

                workout_name = f"{selected_situation.title()} Scenario Drill {RealGameDrillWorkout.objects.filter(situation_type=selected_situation).count() + 1}"
                workout = RealGameDrillWorkout.objects.create(
                    name=workout_name,
                    situation_type=selected_situation  # ✅ este es el campo correcto
                )


                workout.drills.set(selected_drills)
                workout_exercises = selected_drills

        return render(request, 'real_game_drills_generation.html', {
            'scenarios': RealGameDrill.objects.values_list('situation_type', flat=True).distinct(),
            'selected_situation': selected_situation,
            'workout_exercises': workout_exercises
        })

    return render(request, 'real_game_drills_generation.html', {
        'scenarios': RealGameDrill.objects.values_list('situation_type', flat=True).distinct()
    })


def real_game_drills_list(request):
    workouts = RealGameDrillWorkout.objects.all()
    return render(request, 'real_game_drills_list.html', {'workouts': workouts})

def schedule(request, year=None, month=None):
    today = date.today()
    year = year or today.year
    month = month or today.month

    # Matriz de semanas con días del mes (0 si está vacío)
    cal = calendar.Calendar(firstweekday=0)  # 0 = lunes
    month_days = cal.monthdayscalendar(year, month)

    context = {
        'month_days': month_days,
        'month_name': calendar.month_name[month],
        'year': year,
        'month': month,
    }
    return render(request, 'schedule.html', context)

def progress_dashboard(request):
    player_id = request.session.get('player_id')
    if not player_id:
        return redirect('/login/')

    user = player.objects.get(id=player_id)

    # Total de registros
    total_workouts = WorkoutProgress.objects.filter(user=user).count()

    # Promedio y máximo peso levantado
    avg_weight = WorkoutProgress.objects.filter(user=user).aggregate(Avg('weight'))['weight__avg'] or 0
    max_weight = WorkoutProgress.objects.filter(user=user).aggregate(Max('weight'))['weight__max'] or 0

    # Últimos 7 días de actividad
    today = datetime.today().date()
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]

    last_week_progress = []
    for day in last_7_days:
        entries = WorkoutProgress.objects.filter(user=user, date=day)
        total_entries = entries.count()
        avg_weight_day = entries.aggregate(Avg('weight'))['weight__avg'] or 0
        last_week_progress.append({
            'weekday': day.strftime('%a'),  # Lunes = Mon, etc.
            'date': day.strftime('%Y-%m-%d'),  # Fecha completa
            'total': total_entries,
            'avg_weight': avg_weight_day
        })

    return render(request, 'progress_dashboard.html', {
        'total_workouts': total_workouts,
        'avg_weight': avg_weight,
        'max_weight': max_weight,
        'last_week_progress': last_week_progress
    })