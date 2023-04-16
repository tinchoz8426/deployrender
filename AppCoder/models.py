from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Curso(models.Model):
    nombre=models.CharField(max_length=50 )
    comision=models.IntegerField()   
    def __str__(self):
        return f"{self.nombre} - {self.comision}"    

class Estudiante(models.Model):
    nombre=models.CharField(max_length=50)
    apellido=models.CharField(max_length=50)
    email=models.EmailField()
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}" 

class Profesor(models.Model):
    nombre= models.CharField(max_length=50)
    apellido= models.CharField(max_length=50)
    email= models.EmailField()
    profesion= models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} {self.apellido}" 

class Entregable(models.Model):
    nombre= models.CharField(max_length=50)
    fecha_entrega= models.DateField()
    entregado= models.BooleanField()
    
class Avatar(models.Model):
    # vinculo con el usuario
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # subcarpeta avatares de media
    imagen = models.ImageField(upload_to="avatares", null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.imagen}"
