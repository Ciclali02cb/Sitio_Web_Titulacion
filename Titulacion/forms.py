from django import forms
from .models import Titulacion
from .models import Profesor


class TitulacionForm(forms.ModelForm):
    class Meta:
        model = Titulacion
        fields = ['correo','matricula','nombre',  
                  'apellido_paterno', 'apellido_materno', 'carrera','edad', 
                  'titulo_proyecto', 'archivo', 'titulacion_tipo', 'lugar', 
                  'discapacidad', 'genero', 'modalidad' 
        ]

class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = ['sigla','nombreProfesor', 'apellidoPaterno', 'apellidoMaterno', 'cedulaProfesor']