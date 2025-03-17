from django.shortcuts import render, redirect

# Create your views here.
def main(request):
    # Revisar si el player está logueado
    if 'player_id' not in request.session:
        return redirect('/login/')  # Si no hay sesión, redirige al login
    
    # Si el usuario está logueado, muestra la página normal
    return render(request, 'main.html', {
        'username': request.session.get('username')  # Por si quieres mostrarlo en el HTML
    })