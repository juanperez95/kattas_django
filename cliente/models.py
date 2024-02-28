from django.db import models
from django.utils import timezone

class Perfil(models.Model):
    nombre_perfil = models.CharField(max_length=20,null=False)
    
class Habilitado(models.Model):
    nombre_habilitado = models.CharField(max_length=20,null=False)
    
class Cargo(models.Model):
    nombre_cargo = models.CharField(max_length=20,null=False)

# Create your models here.
class Usuario(models.Model):
    documento = models.BigIntegerField(null=False,primary_key=True)
    habilitado = models.ForeignKey(Habilitado,on_delete=models.CASCADE, blank=True, null=True)
    perfil = models.ForeignKey(Perfil,on_delete=models.CASCADE, blank=True, null=True)
    cargo = models.ForeignKey(Cargo,on_delete=models.CASCADE, blank=True, null=True)
    password = models.TextField(null=False)
    nombre = models.CharField(max_length=30,null=False)
    apellidos = models.CharField(max_length=30,null=False)
    email = models.EmailField(null=False)
    fecha_registro = models.DateField(null=False,default=timezone.now)
    fecha_nacimiento = models.DateField(null=False)
    genero = models.CharField(max_length=30,null=False)
    telefono = models.CharField(max_length=10,null=False)

    
    
    