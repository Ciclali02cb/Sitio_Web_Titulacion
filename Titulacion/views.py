from django.shortcuts import render, redirect , get_object_or_404# type: ignore
from .models import Titulacion
from .forms import TitulacionForm
from .models import Profesor
from .forms import ProfesorForm
from django.db.models import Q

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

def update_titulacion(request, pk):
    titulacion = get_object_or_404(Titulacion, pk=pk)
    if request.method == 'POST':
        form = TitulacionForm(request.POST, request.FILES, instance=titulacion)
        if form.is_valid():
            form.save()
            return redirect('lista_titulaciones')  
    else:
        form = TitulacionForm(instance=titulacion)
    return render(request, 'titulacion_form.html', {'form': form, "titulacion" : titulacion})

def delete_titulacion(request, pk):
    titulacion = get_object_or_404(Titulacion, pk=pk)
    if request.method == 'POST':
        titulacion.delete()
        return redirect('lista_titulaciones') 
    else:
        form = TitulacionForm(instance=titulacion)
    return render(request, 'confirmar_eliminar.html', {'titulacion': titulacion})  

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
