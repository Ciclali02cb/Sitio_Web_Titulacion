from django import forms
from .models import Titulacion
from .models import Profesor


class TitulacionForm(forms.ModelForm):
    class Meta:
        model = Titulacion
        fields = ['correo','matricula','nombre','apellido_paterno','apellido_materno',
                  'carrera','edad', 'telefono', 'dialecto','promedio',
                  'nombre_del_proyecto','archivo',
                  'opcion_de_titulacion', 'asesor','revisor_1',
                  'revisor_2','lugar','discapacidad', 'genero','modalidad', 
                  
                  
                   
        ]
        labels = {
            'correo': 'Correo Electrónico',
            'matricula': 'Matrícula',
            'nombre': 'Nombre(s)',
            'apellido_paterno': 'Apellido Paterno',
            'apellido_materno': 'Apellido Materno',
            'carrera': 'Carrera',
            'edad': 'Edad',
            'telefono': 'Telefono',
            'dialecto': 'Dialecto',
            'promedio': 'Promedio',
            'nombre_del_proyecto': 'NOMBRE DEL PROYECTO (Debe respetar el uso de minúsculas y mayúsculas según corresponda)',
            'archivo': 'Adjunta tu proyecto final en formato PDF (el archivo debe pesar máximo 10mb)',
            'opcion_de_titulacion': 'Opción de Titulación',
            'asesor': 'Nombre del Asesor',
            'revisor_1': 'Nombre del Revisor 1',
            'revisor_2': 'Nombre del Revisor 2',
            'lugar': 'Ciudad',
            'discapacidad': '¿Tiene alguna discapacidad?',
            'genero': 'Género',
            'modalidad': 'Modalidad',
        }
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar cómo se muestran los campos de selección de profesores
        self.fields['asesor'].queryset = Profesor.objects.all().order_by('apellidoPaterno')
        self.fields['revisor_1'].queryset = Profesor.objects.all().order_by('apellidoPaterno')
        self.fields['revisor_2'].queryset = Profesor.objects.all().order_by('apellidoPaterno')
        
        # Opcional: cambiar el widget para mostrar mejor los profesores
        self.fields['asesor'].label_from_instance = lambda obj: f"{obj.sigla} {obj.nombreProfesor} {obj.apellidoPaterno} {obj.apellidoMaterno}"
        self.fields['revisor_1'].label_from_instance = lambda obj: f"{obj.sigla} {obj.nombreProfesor} {obj.apellidoPaterno} {obj.apellidoMaterno}"
        self.fields['revisor_2'].label_from_instance = lambda obj: f"{obj.sigla} {obj.nombreProfesor} {obj.apellidoPaterno} {obj.apellidoMaterno}"


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