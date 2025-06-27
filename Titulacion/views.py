from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Titulacion, Acta, Profesor, Director
from .forms import TitulacionForm, ProfesorForm, ActaForm
from django.db.models import Q
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from reportlab.lib.units import inch
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib.units import cm
import os
from django.conf import settings
from reportlab.lib.colors import Color, black
import json

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        
        return JsonResponse({
            'success': False,
            'error': 'Usuario o contraseña incorrectos'
        }, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def home_view(request):
    return render(request, 'titulaciones/index.html')
@login_required
def titulacion_list(request):
    query = request.GET.get('q', '')
    
    if query:
        titulaciones = Titulacion.objects.filter(
            Q(nombre__icontains=query) |
            Q(matricula__icontains=query) |
            Q(apellido_paterno__icontains=query) |
            Q(apellido_materno__icontains=query)
        )
    else:
        titulaciones = Titulacion.objects.all()
    
    context = {
        'titulaciones': titulaciones,
        'query': query
    }
    return render(request, 'titulaciones/titulacion_list.html', context)
@login_required
def update_titulacion(request, pk):
    titulacion = get_object_or_404(Titulacion, pk=pk)
    if request.method == 'POST':
        form = TitulacionForm(request.POST, request.FILES, instance=titulacion)
        if form.is_valid():
            # Elimina el archivo anterior si se sube uno nuevo
            if 'archivo' in request.FILES:
                if titulacion.archivo:
                    titulacion.archivo.delete()
            form.save()
            return redirect('titulacion_list')
    else:
        form = TitulacionForm(instance=titulacion)
    
    return render(request, 'titulacion/titulacion_form.html', {
        'form': form,
        'titulacion': titulacion
    })
@login_required    
def delete_titulacion(request, pk):
    titulacion = get_object_or_404(Titulacion, pk=pk)
    if request.method == 'POST':
        titulacion.delete()
        return redirect('titulacion_list') 
    else:
        form = TitulacionForm(instance=titulacion)
    return render(request, 'titulaciones/confirm_eliminar.html', {'titulacion': titulacion})  

def confirm_titulacion(request):
    return render(request, 'titulaciones/confirm_titulacion.html')
def create_titulacion(request):
    if request.method == 'POST':
        form = TitulacionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            #return redirect('titulacion_list')
            archivo = form.cleaned_data['archivo']
            return redirect('confirm_titulacion')
    else:
        form = TitulacionForm()
    return render(request, 'titulaciones/titulacion_form.html', {'form': form})

#PROFESORES EN EL ITSA
# Vista para listar profesores
@login_required
def lista_profesores(request):
    query = request.GET.get('query', '')
    
    if query:
        profesores = Profesor.objects.filter(
            Q(nombreProfesor__icontains=query) | 
            Q(cedulaProfesor__icontains=query))
    else:
        profesores = Profesor.objects.all()
    
    context = {
        'profesores': profesores,
        'query': query
    }
    return render(request, 'titulaciones/profesor_list.html', context)

# Vista para agregar un nuevo profesor
@login_required
def agregar_profesor(request):
    if request.method == 'POST':
        form = ProfesorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_profesores')
    else:
        form = ProfesorForm()
    return render(request, 'titulaciones/profesor_form.html', {'form': form})

@login_required
def update_profesor(request, pk):
    profesor = get_object_or_404(Profesor, pk=pk)
    if request.method == 'POST':
        form = ProfesorForm(request.POST, instance=profesor)
        if form.is_valid():
            form.save()
            return redirect('lista_profesores')
    else:
        form = ProfesorForm(instance=profesor)
    return render(request, 'titulaciones/profesor_form.html', {'form': form})
@login_required
def delete_profesor(request, pk):
    profesor = get_object_or_404(Profesor, pk=pk)
    if request.method == 'POST':
        profesor.delete()
        return redirect('lista_profesores')
    return render(request, 'titulaciones/confirm_delete_profesor.html', {'profesor': profesor})

def acta_Alumno(request, pk):
    alumno = get_object_or_404(Titulacion, pk=pk)
    acta = alumno.acta  # Esto funciona por la relación OneToOne
    
    context = {
        'alumno': alumno,
        'acta': acta,  # Asegúrate de pasar el objeto acta al contexto
    }
    return render(request, 'acta_Alumno.html', context)

def acta_form_view(request):
    alumnos = Titulacion.objects.select_related('acta').all()
    if request.method == 'POST':
        # Procesar los datos del formulario
        for alumno in alumnos:
            acta, created = Acta.objects.get_or_create(titulacion=alumno)
            form = ActaForm(request.POST, instance=acta, prefix=str(alumno.pk))
            if form.is_valid():
                form.save()
        return redirect('acta_form_view')
    
    context = {
        'alumnos': alumnos,
    }
    return render(request, 'titulaciones/acta_form.html', context)
@login_required
@csrf_exempt
def guardar_acta(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            matricula = data.get('matricula')
            
            # Buscar el registro de titulación por matrícula
            try:
                titulacion = Titulacion.objects.get(matricula=matricula)
            except Titulacion.DoesNotExist:
                return JsonResponse({
                    'success': False, 
                    'error': f'No se encontró un alumno con la matrícula {matricula}'
                }, status=404)
            
            # Crear o actualizar el acta
            acta, created = Acta.objects.get_or_create(titulacion=titulacion)
            
            # Actualizar campos del acta
            campos_acta = [
                'dia_examen', 'mes_examen', 'anio_examen',
                'hora_inicio', 'dictamen', 'hora_fin',
                'libro', 'foja', 'dia_firma',
                'mes_firma', 'anio_firma', 'dia_firmma',
                'mes_firma_final', 'anio_firmma'
            ]
            
            for campo in campos_acta:
                if campo in data:
                    setattr(acta, campo, data.get(campo))
            
            acta.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Acta guardada correctamente'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False, 
                'error': 'Formato JSON inválido'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'error': f'Error en el servidor: {str(e)}'
            }, status=500)
    
    return JsonResponse({
        'success': False, 
        'error': 'Método no permitido. Se requiere POST'
    }, status=405)

def acta_form_view(request):
    # Obtener parámetros de búsqueda
    search_query = request.GET.get('q', '')
    tipo_titulacion = request.GET.get('tipo', 'todas')
    
    # Obtener todos los alumnos con sus actas relacionadas
    alumnos = Titulacion.objects.select_related('acta', 'asesor', 'revisor_1', 'revisor_2').all()
    
    # Aplicar filtro de búsqueda si hay término
    if search_query:
        alumnos = alumnos.filter(
            Q(matricula__icontains=search_query) |
            Q(nombre__icontains=search_query) |
            Q(apellido_paterno__icontains=search_query) |
            Q(apellido_materno__icontains=search_query)
        )
    
    # Aplicar filtro por tipo de titulación
    if tipo_titulacion != 'todas':
        if tipo_titulacion == 'Examen General':
            alumnos = alumnos.filter(opcion_de_titulacion__contains='Examen General de Egreso')
        else:
            alumnos = alumnos.filter(opcion_de_titulacion=tipo_titulacion)
    
    # Obtener datos del director
    director = Director.objects.first()
    if not director:
        director = {
            'sigla': 'DR.',
            'nombre': 'Ricardo',
            'apellidos': 'Ávila García'
        }
    
    context = {
        'alumnos': alumnos,
        'director': director,
        'request': request
    }
    
    return render(request, 'titulaciones/acta_form.html', context)

def acta_alumno_view(request, pk):
    alumno = get_object_or_404(Titulacion, pk=pk)
    return render(request, 'titulaciones/Acta_Alumno.html', {'alumno': alumno})

@csrf_exempt
def guardar_director(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            director, created = Director.objects.get_or_create(id=1)
            director.sigla = data.get('sigla', 'DR.')
            director.nombre = data.get('nombre', '')
            director.apellidos = data.get('apellidos', '')
            director.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})