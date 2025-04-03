from django.shortcuts import render, redirect , get_object_or_404
from .models import Titulacion
from .forms import TitulacionForm
from .models import Profesor
from .forms import ProfesorForm

def home_view(request):
    return render(request, 'titulaciones/index.html')
def titulacion_list(request):
    titulaciones = Titulacion.objects.all()
    context = {
        'titulaciones': titulaciones
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


def buscar_titulaciones(request):
    query = request.GET.get('query', '')  # Obtiene el valor de búsqueda del formulario
    resultados = Titulacion.objects.filter(
        nombre__icontains=query
    ) | Titulacion.objects.filter(
        correo__icontains=query
    ) | Titulacion.objects.filter(
        matricula__icontains=query
    ) | Titulacion.objects.filter(
        carrera__icontains=query
    ) | Titulacion.objects.filter(
        titulo_proyecto__icontains=query
    ) if query else Titulacion.objects.all()

    return render(request, 'buscar_titulaciones.html', {'resultados': resultados, 'query': query})

#PROFESORES EN EL ITSA
# Vista para listar profesores
def lista_profesores(request):
    profesores = Profesor.objects.all()
    context = {
        'profesores': profesores
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