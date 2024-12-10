from django.urls import path
from .views import home, create_task, mapa, signin, signup, tasks, signout
from . import views


urlpatterns = [
    path('', home, name='home'),
    path('create_task/', create_task, name='create_task'),
    path('mapa/', mapa, name='mapa'),
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('tasks/', tasks, name='tasks'),
    path('actualizar-tarea/', views.actualizar_tarea, name='actualizar_tarea'),
    path('eliminar_tarea/', views.eliminar_tarea, name='eliminar_tarea'),
    path('create_task/', views.create_task, name='create_task'),
    path('logout/', signout, name='logout'),
]