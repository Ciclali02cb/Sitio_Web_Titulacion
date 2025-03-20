from django.db import models # type: ignore

# Create your models here.


class Titulacion(models.Model):
    correo = models.EmailField(max_length = 254) 
    matricula = models.CharField(max_length=8) 
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100, default="")
    apellido_materno = models.CharField(max_length=100, default="")
    edad = models.IntegerField(default=0)
    titulo_proyecto = models.CharField(max_length=200, default="")
    archivo = models.FileField(upload_to='archivo')
    carrera = models.CharField(max_length=100, choices=[
        ('INGENIERÍA BIOQUÍMICA', 'INGENIERÍA BIOQUÍMICA'),
        ('INGENIERÍA CIVIL', 'INGENIERÍA CIVIL'),
        ('INGENIERÍA ELECTROMECÁNICA', 'INGENIERÍA ELECTROMECÁNICA'),
        ('GESTIÓN EMPRESARIAL', 'GESTIÓN EMPRESARIAL'),
        ('INGENIERÍA DE SISTEMAS COMPUTACIONALES', 'INGENIERÍA DE SISTEMAS COMPUTACIONALES'),
        ('INGENIERÍA INDUSTRIAL', 'INGENIERÍA INDUSTRIAL'),
        ('INGENIERÍA INFORMÁTICA', 'INGENIERÍA INFORMÁTICA'),
        ('INGENIERÍA MECATRÓNICA', 'INGENIERÍA MECATRÓNICA'),
        ('INGENIERÍA QUÍMICA', 'INGENIERÍA QUÍMICA'),
        ('LICENCIATURA EN INFORMÁTICA', 'LICENCIATURA EN INFORMÁTICA'),
        ],default='INGENIERÍA BIOQUÍMICA')
    titulacion_tipo = models.CharField(
        max_length=25,
        choices=[
            ('Residencia profesional', 'Residencia profesional'),
            ('Tesis', 'Tesis'),
            ('Otro', 'Otro'),
            ],default='Residencia profesional')  
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
        ('Extensión Uxpanapan', 'Extensión Uxpanapan')
        ],default='Escolarizado')
        
    def __str__(self):
        return f"{self.correo} {self.matricula}{self.nombre} {self.carrera} {self.apellido_paterno} {self.titulo_proyecto} {self.apellido_materno} {self.edad} {self.titulacion_tipo} {self.discapacidad} {self.genero} {self.modalidad} "
    
class Profesor (models.Model):
    sigla = models.CharField(max_length=10, default="")
    nombreProfesor = models.CharField(max_length=100)
    apellidoPaterno = models.CharField(max_length=100, default="")
    apellidoMaterno = models.CharField(max_length=100, default="")
    cedulaProfesor = models.IntegerField()
    
    def __str__(self):
        return f"{self.sigla} {self.nombreProfesor} {self.cedulaProfesor} {self.apellidoMaterno} {self.apellidoMaterno}"