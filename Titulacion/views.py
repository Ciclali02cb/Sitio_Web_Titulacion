from django.shortcuts import render, redirect , get_object_or_404
from .models import Titulacion
from .forms import TitulacionForm
from .models import Profesor
from .forms import ProfesorForm
from .models import Acta
from .forms import ActaForm
from django.db.models import Q

def home_view(request):
    return render(request, 'titulaciones/index.html')
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
def agregar_profesor(request):
    if request.method == 'POST':
        form = ProfesorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_profesores')
    else:
        form = ProfesorForm()
    return render(request, 'titulaciones/profesor_form.html', {'form': form})

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