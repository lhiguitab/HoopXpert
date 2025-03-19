from django.shortcuts import render, redirect
from workout.models import Exercise

# Create your views here.
def main(request):
    # Revisar si el player está logueado
    if 'player_id' not in request.session:
        return redirect('/login/')  # Si no hay sesión, redirige al login
    
    # Si el usuario está logueado, muestra la página normal
    return render(request, 'main.html', {'username': request.session.get('username')}) # Por si quieres mostrarlo en el HTML

def exercise(request):
    exercises = Exercise.objects.all()
    return render(request, 'workout_generation.html', {'exercises': exercises})  # Página de ejercicio