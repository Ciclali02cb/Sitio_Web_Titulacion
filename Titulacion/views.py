from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Titulacion
from .forms import TitulacionForm
from .models import Profesor
from .forms import ProfesorForm
from .models import Acta
from .forms import ActaForm
from django.db.models import Q

from django.http import JsonResponse
from django.contrib.auth import authenticate, login

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
    titulacion = get_object_or_404(Titulacion, pk=pk)
    context = {
        'titulacion': titulacion,
        
    }
    return render(request, 'titulaciones/Acta_alumno.html', context)

def acta_alumno_view(request, id):
    acta = get_object_or_404(Acta, id=id)
    titulacion = acta.titulacion  # Asegúrate de que esta relación existe
    
    if request.method == 'POST':
        form = ActaForm(request.POST, instance=acta)
        if form.is_valid():
            form.save()
            return redirect('titulacion_list')  # Ajusta esto según tu necesidad
    else:
        form = ActaForm(instance=acta)
    
    return render(request, 'Acta_alumno.html', {
        'form': form,
        'acta': acta,
        'titulacion': titulacion  # Pasar el objeto titulación al template
    })
    
@login_required
def guardar_acta(request, pk):
    titulacion = get_object_or_404(Titulacion, pk=pk)
    
    if request.method == 'POST':
        # Verificar si ya existe un acta para esta titulación
        try:
            acta = Acta.objects.get(titulacion=titulacion)
            # Si existe, actualizamos sus campos
            acta.dia_examen = request.POST.get('dia_examen', '1')
            acta.mes_examen = request.POST.get('mes_examen', 'enero')
            acta.anio_examen = request.POST.get('anio_examen', '2025')
            acta.hora_inicio = request.POST.get('hora_inicio', '12:00')
            acta.dictamen = request.POST.get('dictamen', 'Aprobado')
            acta.hora_fin = request.POST.get('hora_fin', '13:00')
            acta.libro = request.POST.get('libro', '1')
            acta.foja = request.POST.get('foja', '1')
            acta.dia_firma = request.POST.get('dia_firma', '1')
            acta.mes_firma = request.POST.get('mes_firma', 'enero')
            acta.anio_firma = request.POST.get('anio_firma', '2025')
            acta.dia_firmma = request.POST.get('dia_firmma', '1')
            acta.mes_firma_final = request.POST.get('mes_firma_final', 'enero')
            acta.anio_firmma = request.POST.get('anio_firmma', '2025')
            acta.nombre_director = request.POST.get('nombre_director', 'DR. Ricardo Ávila García.')
            acta.save()
        except Acta.DoesNotExist:
            # Si no existe, creamos una nueva
            Acta.objects.create(
                titulacion=titulacion,
                dia_examen=request.POST.get('dia_examen', '1'),
                mes_examen=request.POST.get('mes_examen', 'enero'),
                anio_examen=request.POST.get('anio_examen', '2025'),
                hora_inicio=request.POST.get('hora_inicio', '12:00'),
                dictamen=request.POST.get('dictamen', 'Aprobado'),
                hora_fin=request.POST.get('hora_fin', '13:00'),
                libro=request.POST.get('libro', '1'),
                foja=request.POST.get('foja', '1'),
                dia_firma=request.POST.get('dia_firma', '1'),
                mes_firma=request.POST.get('mes_firma', 'enero'),
                anio_firma=request.POST.get('anio_firma', '2025'),
                dia_firmma=request.POST.get('dia_firmma', '1'),
                mes_firma_final=request.POST.get('mes_firma_final', 'enero'),
                anio_firmma=request.POST.get('anio_firmma', '2025'),
                nombre_director=request.POST.get('nombre_director', 'DR. Ricardo Ávila García.')
            )
        return redirect('titulacion_list')
    
    # Para solicitudes GET
    try:
        acta = Acta.objects.get(titulacion=titulacion)
        form_data = {
            'dia_examen': acta.dia_examen,
            'mes_examen': acta.mes_examen,
            'anio_examen': acta.anio_examen,
            'hora_inicio': acta.hora_inicio,
            'dictamen': acta.dictamen,
            'hora_fin': acta.hora_fin,
            'libro': acta.libro,
            'foja': acta.foja,
            'dia_firma': acta.dia_firma,
            'mes_firma': acta.mes_firma,
            'anio_firma': acta.anio_firma,
            'dia_firmma': acta.dia_firmma,
            'mes_firma_final': acta.mes_firma_final,
            'anio_firmma': acta.anio_firmma,
            'nombre_director': acta.nombre_director
        }
    except Acta.DoesNotExist:
        form_data = {
            'dia_examen': '1',
            'mes_examen': 'enero',
            'anio_examen': '2025',
            'hora_inicio': '12:00',
            'dictamen': 'Aprobado',
            'hora_fin': '13:00',
            'libro': '1',
            'foja': '1',
            'dia_firma': '1',
            'mes_firma': 'enero',
            'anio_firma': '2025',
            'dia_firmma': '1',
            'mes_firma_final': 'enero',
            'anio_firmma': '2025',
            'nombre_director': 'DR. Ricardo Ávila García'
        }
    
    context = {
        'titulacion': titulacion,
        'form': form_data
    }
    return render(request, 'titulaciones/Acta_alumno.html', context)