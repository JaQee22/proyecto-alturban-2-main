from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse
from .forms import TaskForm
from .models import Task
import folium
from folium.plugins import FastMarkerCluster
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

# Create your views here.

# Vista home.
def home(request):
    return render(request, 'home.html')

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        print("Datos del formulario:", form.data)

        if form.is_valid():
            # Acceder a cleaned_data solo después de que el formulario sea válido
            latitud = form.cleaned_data.get('latitud')
            longitud = form.cleaned_data.get('longitud')

            # Redondeamos latitud y longitud a 6 decimales
            if latitud:
                latitud = round(latitud, 6)
            if longitud:
                longitud = round(longitud, 6)

            # Asignar latitud y longitud redondeados a los datos del formulario
            task = form.save(commit=False)
            task.latitud = latitud
            task.longitud = longitud
            task.user = request.user
            task.save()

            return redirect('tasks')
        else:
            print("Errores del formulario:", form.errors)
            return render(request, 'create_task.html', {'form': form, 'error': 'Por favor, corrige los errores del formulario.'})

    else:
        form = TaskForm()
        return render(request, 'create_task.html', {'form': form})




def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                #Registro del usuario
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'El usuario ya Existe'
                })
        return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Las contraseñas no coinciden'})
    

@login_required
def tasks(request):
    tasks = Task.objects.all()
    return render(request, 'tasks.html', {'tasks': tasks})


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user =authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o Contraceña incorrecta'
            })
        
        else:
            login(request, user)
            return redirect('tasks')
        

@login_required
def mapa(request):

    # Recupero todas las sucursales
    locations = Task.objects.all()

    # Defino el mapa
    initialMap = folium.Map(location=[-33.45694, -70.64827], zoom_start=11)

    for location in locations:
        coordinates = (location.latitud, location.longitud)
        folium.Marker(coordinates, popup='Usuario '+ location.user.username +'Descripción '+ location.descripcion +'Estado '+ location.estado).add_to(initialMap)


    context = {'map':initialMap._repr_html_(), 'locations': locations}
    return render(request, 'mapa.html', context)


# Actualizar Task
def obtener_tarea(request, id):
    tarea = Task.objects.get(id=id)
    data = {
        'id': tarea.id,
        'descripcion': tarea.descripcion,
        'estado': tarea.estado,
    }
    return JsonResponse(data)


def actualizar_tarea(request):
    if request.method == 'POST':
        try:
            task_id = request.POST.get('id')
            descripcion = request.POST.get('descripcion')
            estado = request.POST.get('estado')
            
            # Verifica que los datos necesarios están presentes
            if not task_id or not descripcion or not estado:
                raise ValueError("Faltan datos para actualizar la tarea.")

            # Obtener la tarea y actualizar los campos
            tarea = get_object_or_404(Task, id=task_id)
            tarea.descripcion = descripcion
            tarea.estado = estado
            tarea.save()
            
            # Agregar un mensaje de éxito (opcional)
            messages.success(request, "Tarea actualizada con éxito.")
        
        except Task.DoesNotExist:
            messages.error(request, "La tarea no existe.")
            return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirige al origen
            
        except ValueError as e:
            messages.error(request, str(e))
            return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirige al origen
        
        except Exception as e:
            # Captura cualquier otro error inesperado
            messages.error(request, f"Error al actualizar la tarea: {str(e)}")
            return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirige al origen

        # Redirigir a la misma página desde donde se realizó la solicitud
        return redirect(request.META.get('HTTP_REFERER', '/'))

    else:
        return HttpResponse('Método no permitido', status=405)
    

#Eliminar Registro
def eliminar_tarea(request):
    if request.method == 'POST':
        task_id = request.POST['id']
        
        # Obtener la tarea y eliminarla
        tarea = get_object_or_404(Task, id=task_id)
        tarea.delete()
        
        # Redirigir a la misma página
        return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirige a la misma página o al home
    else:
        return HttpResponse('Método no permitido', status=405)
