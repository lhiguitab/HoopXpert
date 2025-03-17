from django.shortcuts import render, redirect
from django.db import models
from .models import player

# Create your views here.
def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get("username").strip()
        password = request.POST.get("password").strip()

        try:
            jugador = player.objects.get(username=username)

            if jugador.password == password:
                request.session['player_id'] = jugador.id
                request.session['username'] = jugador.username

                return redirect('/main/')

        except player.DoesNotExist:
            pass

        # Si falla por usuario o password
        return render(request, 'login.html', {
            'error': 'Username or password may be wrong'
        })

    return render(request, 'login.html')

def signup(request):
    if request.method == "POST":
        # Extraer datos del formulario
        name = request.POST.get("name")
        age = request.POST.get("age")
        height = request.POST.get("height")
        weight = request.POST.get("weight")
        position = request.POST.get("position")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Verificar si ya existe un usuario con el mismo username, email o password
        existing_player = player.objects.filter(
            models.Q(username=username) |
            models.Q(email=email) |
            models.Q(password=password)
        ).first()

        if existing_player:
            # Ya existe uno, no dejamos continuar
            return render(request, 'signup.html', {
                'error': 'Username, email or password already in use'
            })

        # Crear una nueva instancia del modelo y guardarla
        new_player = player(
            name=name,
            age=age,
            height=height,
            weight=weight,
            position=position,
            email=email,
            username=username,
            password=password
        )
        new_player.save()

        # Redirige al login o a la página principal
        return redirect('/login/')  # O a donde quieras

    return render(request, 'signup.html')

def logout(request):
    request.session.flush()  # Borra todos los datos de la sesión
    return redirect('/login/')