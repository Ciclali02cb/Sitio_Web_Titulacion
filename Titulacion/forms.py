from django import forms
from .models import Titulacion
from .models import Profesor


class TitulacionForm(forms.ModelForm):
    class Meta:
        model = Titulacion
        fields = ['correo','matricula','nombre','apellido_paterno','apellido_materno',
                  'carrera','edad','promedio','nombre_del_proyecto','archivo',
                  'opcion_de_titulacion', 'nombre_del_asesor','nombre_del_revisor_1',
                  'nombre_del_revisor_2','lugar','discapacidad', 'genero','modalidad', 'dialecto',  
        ]
        labels = {
            'correo': 'Correo Electrónico',
            'matricula': 'Matrícula',
            'nombre': 'Nombre(s)',
            'apellido_paterno': 'Apellido Paterno',
            'apellido_materno': 'Apellido Materno',
            'carrera': 'Carrera',
            'edad': 'Edad',
            'promedio': 'Promedio',
            'nombre_del_proyecto': 'NOMBRE DEL PROYECTO (Debe respetar el uso de minúsculas y mayúsculas según corresponda)',
            'archivo': 'Adjunta tu proyecto final en formato PDF (el archivo debe pesar máximo 10mb)',
            'opcion_de_titulacion': 'Opción de Titulación',
            'nombre_del_asesor': 'Nombre del Asesor',
            'nombre_del_revisor_1': 'Nombre del Revisor 1',
            'nombre_del_revisor_2': 'Nombre del Revisor 2',
            'lugar': 'Ciudad',
            'discapacidad': '¿Tiene alguna discapacidad?',
            'genero': 'Género',
            'modalidad': 'Modalidad',
            'dialecto' : 'Dialecto',
        }

class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = ['sigla','nombreProfesor', 'apellidoPaterno', 'apellidoMaterno', 'cedulaProfesor']
        labels = {
            'sigla': 'Nivel Academico',
            'nombreProfesor': 'Nombre',
            'apellidoPaterno': 'Apellido Paterno',
            'apellidoMaterno': 'Apellido Materno',
            'cedulaProfesor': 'Cédula',
        }