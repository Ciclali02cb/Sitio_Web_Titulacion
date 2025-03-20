from django.shortcuts import render, redirect # type: ignore
from .models import Titulacion
from .forms import TitulacionForm
from .models import Profesor
from .forms import ProfesorForm

def titulacion_list(request):
    titulaciones = Titulacion.objects.all()
    context = {
        'titulaciones': titulaciones
    }
    return render(request, 'titulaciones/titulacion_list.html', context)

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
