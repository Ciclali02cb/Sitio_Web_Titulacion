from django.db import models 
from django.utils.safestring import mark_safe
from django.core.validators import RegexValidator

class Profesor (models.Model):
    sigla = models.CharField(max_length=50, choices=[
        ('MTI.', 'Maestría en Tecnologías de la Información'),
        ('MDIS.', 'Maestría en Diseño'),
        ('ING.', 'Ingeniero'),
        ('LIC.', 'Licenciado'),
        ('DR.', 'Doctor')], default='MTI')
    nombreProfesor = models.CharField(max_length=100)
    apellidoPaterno = models.CharField(max_length=100, default="")
    apellidoMaterno = models.CharField(max_length=100, default="")
    cedulaProfesor = models.IntegerField()
    phone_validator = RegexValidator(regex=r'^\d{10}$',message="El número de teléfono debe contener exactamente 10 dígitos.")
    telefono_prof = models.CharField(
        max_length=10,
        validators=[phone_validator],
        blank=True, 
        null=True,
        help_text="Debe contener exactamente 10 dígitos"
    )
    email_prof = models.EmailField(blank=True, null=True)
    def __str__(self):
        return f"{self.sigla} {self.nombreProfesor} {self.cedulaProfesor} {self.apellidoMaterno} {self.apellidoMaterno} {self.telefono} "

class Titulacion(models.Model):
    correo = models.EmailField(max_length = 254) 
    matricula = models.CharField(max_length=8, unique=True) 
    nombre = models.CharField(max_length=100, help_text=mark_safe('<span style="color: red;">Escrito en Mayúsculas</span>'))
    apellido_paterno = models.CharField(max_length=100, default="", help_text=mark_safe('<span style="color: red;">Escrito en Mayúsculas</span>'))
    apellido_materno = models.CharField(max_length=100, default="", help_text=mark_safe('<span style="color: red;">Escrito en Mayúsculas</span>'))
    edad = models.IntegerField(default=0)
    promedio = models.IntegerField(default=0)
    nombre_del_proyecto = models.CharField(max_length=205, default="", help_text=mark_safe('<span style="color: red; ">Debe respetar el uso de minúsculas y mayúsculas según corresponda</span>'))
    archivo = models.FileField(upload_to='archivo', help_text=mark_safe('<span style="color: red; ">Adjunta tu proyecto final en formato PDF (el archivo debe pesar máximo 10MB)</span>'))
    phone_validator = RegexValidator(regex=r'^\d{10}$',message="El número de teléfono debe contener exactamente 10 dígitos.")
    telefono = models.CharField(max_length=10, validators=[phone_validator], blank=True, null=True, help_text="Debe contener exactamente 10 dígitos")
    dialecto = models.CharField(max_length=100,blank=True,null=True,verbose_name="¿Cuál dialecto?")
    carrera = models.CharField(max_length=100, choices=[
        ('INGENIERÍA BIOQUÍMICA', 'INGENIERÍA BIOQUÍMICA'),
        ('INGENIERÍA CIVIL', 'INGENIERÍA CIVIL'),
        ('INGENIERÍA ELECTROMECÁNICA', 'INGENIERÍA ELECTROMECÁNICA'),
        ('INGENIERÍA EN GESTIÓN EMPRESARIAL', 'INGENIERÍA EN GESTIÓN EMPRESARIAL'),
        ('INGENIERÍA DE SISTEMAS COMPUTACIONALES', 'INGENIERÍA DE SISTEMAS COMPUTACIONALES'),
        ('INGENIERÍA INDUSTRIAL', 'INGENIERÍA INDUSTRIAL'),
        ('INGENIERÍA INFORMÁTICA', 'INGENIERÍA INFORMÁTICA'),
        ('INGENIERÍA MECATRÓNICA', 'INGENIERÍA MECATRÓNICA'),
        ('INGENIERÍA QUÍMICA', 'INGENIERÍA QUÍMICA'),
        ('LICENCIATURA EN INFORMÁTICA', 'LICENCIATURA EN INFORMÁTICA'),
        ],default='INGENIERÍA BIOQUÍMICA')
    opcion_de_titulacion = models.CharField(
        max_length=150, choices=[
        ('Residencia Profesional', 'Residencia Profesional'),
        ('Proyecto de Investigación y/o Desarrollo Tecnológico', 'Proyecto de Investigación y/o Desarrollo Tecnológico'),
        ('Proyecto Integrador','Proyecto Integrador'),
        ('Proyecto Productivo','Proyecto Productivo'),
        ('Proyecto de Innovación Tecnológica','Proyecto de Innovación Tecnológica'),
        ('Proyecto de Emprededurismo','Proyecto de Emprededurismo'),
        ('Estancia','Estancia'),
        ('Tesis o Tesina', 'Tesis o Tesina'),
        ('Examen General de Egreso de Licenciatura (EGEL) del Centro Nacional de Evaluación para la Educación Superior, A.C(CENEVAL)','Examen General de Egreso de Licenciatura (EGEL) del Centro Nacional de Evaluación para la Educación Superior, A.C(CENEVAL)'),
        ],default='Residencia Profesional') 
    asesor = models.ForeignKey(
        Profesor, 
        on_delete=models.SET_NULL, 
        related_name='asesorados',
        null=True, 
        blank=True,
        verbose_name="Asesor"
    )
        
    revisor_1 = models.ForeignKey(
        Profesor, 
        on_delete=models.SET_NULL, 
        related_name='revisiones_1',
        null=True, 
        blank=True,
        verbose_name="Revisor 1"
    )
        
    revisor_2 = models.ForeignKey(
        Profesor, 
        on_delete=models.SET_NULL, 
        related_name='revisiones_2',
        null=True, 
        blank=True,
        verbose_name="Revisor 2"
    )

    lugar = models.CharField(max_length=100, choices=[
        ('Acayucan', 'Acayucan'),
        ('Oluta', 'Oluta'),
        ('Jaltipan','Jaltipan'),
        ('Texistepec', 'Texistepec'),
        ('Cosoleacaque', 'Cosoleacaque'),
        ('Hueyapan','Hueyapan'),
        ('Covarrubias','Covarrubias'),
        ('Otro', 'Otro')
        ],default= 'Acayucan')
    discapacidad = models.CharField(max_length=100, choices=[
        ('Si', 'Si'),
        ('No', 'No')
        ],default='Si')
    genero = models.CharField(max_length=100, choices=[
        ('Hombre', 'Hombre'),
        ('Mujer', 'Mujer')
        ],default='Hombre')
    modalidad = models.CharField(max_length=100, choices=[
        ('Escolarizado', 'Escolarizado'),
        ('Sabatino', 'Sabatino'),
        ('Dominical','Dominical'),
        ('Extensión Hueyapan', 'Extensión Hueyapan'),
        ('Extensión Uxpanapan', 'Extensión Uxpanapan'),
        ('En Línea', 'En Linea')
        ],default='Escolarizado')
    periodo_escolar_Inicio = models.CharField(
    max_length=20,
    help_text=mark_safe('<span style="color: red; ">Formato: MES/AÑO (ej. AGOSTO-2022)</span>'),
    default="AGOSTO/2022"  
    )
    periodo_escolar_Final = models.CharField(
    max_length=20,
    help_text=mark_safe('<span style="color: red; ">Formato: MES/AÑO (ej. DICIEMBRE-2025) (100 CREDITOS ACOMULADOS) </span>'),
    default="DICIEMBRE/2025"  
    )
    
    def __str__(self):
        return f"{self.correo} {self.matricula}{self.nombre} {self.carrera} {self.apellido_paterno} {self.nombre_del_proyecto} {self.apellido_materno}  {self.edad} {self.promedio} {self.opcion_de_titulacion} {self.asesor}{self.revisor_1}{self.revisor_2} {self.discapacidad} {self.genero} {self.modalidad} {self.dialecto} {self.telefono} {self.periodo_escolar_Inicio} {self.periodo_escolar_Final}"
    
class Acta(models.Model):
    # Relación con Titulacion (OneToOne porque cada titulación tendrá un acta)
    titulacion = models.OneToOneField(
        Titulacion,
        on_delete=models.CASCADE,
        related_name='acta',
        unique=True
    )  
    # Campos para la fecha del examen
    dia_examen = models.CharField(max_length=2, default='1', blank=True, null=True)
    mes_examen = models.CharField(max_length=20, default='enero', blank=True, null=True)
    anio_examen = models.CharField(max_length=4, default='2025', blank=True, null=True)
    
    # Horarios
    hora_inicio = models.CharField(max_length=5, default='12:00', blank=True, null=True)
    hora_fin = models.CharField(max_length=5, default='13:00', blank=True, null=True)
    
    # Dictamen
    dictamen = models.CharField(max_length=50, default='Aprobado', blank=True, null=True)
    
    # Datos del libro de actas
    libro = models.CharField(max_length=50, default='1', blank=True, null=True)
    foja = models.CharField(max_length=50, default='1', blank=True, null=True)
    
    # Fecha de firma
    dia_firma = models.CharField(max_length=2, default='1', blank=True, null=True)
    mes_firma = models.CharField(max_length=15, default='enero', blank=True, null=True)
    anio_firma = models.CharField(max_length=4, default='2025', blank=True, null=True)
    
    # Fecha final (para "usos legales")
    dia_firmma = models.CharField(max_length=2, default='1', blank=True, null=True)
    mes_firma_final = models.CharField(max_length=15, default='enero', blank=True, null=True)
    anio_firmma = models.CharField(max_length=4, default='2025', blank=True, null=True)
    
    # Director
    nombre_director = models.CharField(
        max_length=100, 
        default='DR. Ricardo Ávila García.',
        blank=True,
        null=True
    )
    class Meta:
        verbose_name = 'Acta de Titulación'
        verbose_name_plural = 'Actas de Titulación'

    def __str__(self):
        return f"Acta de {self.titulacion.nombre}"
    
    def delete(self, *args, **kwargs):
        # Elimina el archivo cuando se borra el objeto
        if self.archivo:
            storage, path = self.archivo.storage, self.archivo.path
            storage.delete(path)
        super().delete(*args, **kwargs)
        
class Director(models.Model):
    sigla = models.CharField(max_length=10, default='DR.')
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.sigla} {self.nombre} {self.apellidos}"