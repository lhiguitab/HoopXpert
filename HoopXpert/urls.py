"""
URL configuration for HoopXpert project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user import views as user_views
from workout import views as workout_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.home),
    path('login/', user_views.login),
    path('signup/', user_views.signup),
    path('logout/', user_views.logout),
    path('main/', workout_views.main),
    path('workout/', workout_views.exercise),
    path('workout_list/', workout_views.workout_list),
    path('track_progress/', workout_views.track_progress),
    path('routine_improvement/', workout_views.routine_improvement),
    path('basketball_drills/', workout_views.basketball_drills),
    path('drills_list/', workout_views.drills_list),
    path('real_game_drills/', workout_views.real_game_drills),
    path('real_game_drills_list/', workout_views.real_game_drills_list),
    path('schedule/', workout_views.schedule),

]
