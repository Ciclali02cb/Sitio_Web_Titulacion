from django import forms
from .models import Titulacion
from .models import Profesor


class TitulacionForm(forms.ModelForm):
    class Meta:
        model = Titulacion
        fields = ['correo','matricula','nombre','apellido_paterno','apellido_materno',
                  'carrera','edad','promedio','nombre_del_proyecto','archivo',
                  'opcion_de_titulacion', 'nombre_del_asesor','nombre_del_revisor_1','nombre_del_revisor_2','lugar','discapacidad', 'genero','modalidad',   
        ]

class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = ['sigla','nombreProfesor', 'apellidoPaterno', 'apellidoMaterno', 'cedulaProfesor']
        labels = {
            'sigla': 'Sigla',
            'nombreProfesor': 'Nombre',
            'apellidoPaterno': 'Apellido Paterno',
            'apellidoMaterno': 'Apellido Materno',
            'cedulaProfesor': 'Cédula',
        }