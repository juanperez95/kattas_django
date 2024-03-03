from django.shortcuts import render, redirect
from cliente.models import *

def dashboard_base(request):
    return render(request,"cliente/dashboard.html")

def dashboard_insumos(request):
    return render(request,"cliente/dashboard_insumo.html")

def dashboard_usuarios(request):
    return render(request,"cliente/dashboard_usuarios.html")

def dashboard_productos(request):
    return render(request,"cliente/dashboard_productos.html")
    
def actualizar_usuario(request, id):
    if request.method == 'POST':
        usuario = Usuario.objects.get(documento=id)
        usuario.documento = request.POST['documento']
        usuario.nombre = request.POST['Nombre']
        usuario.apellidos = request.POST['apellido']
        usuario.direccion = request.POST['direccion']
        usuario.email = request.POST['email']
        usuario.telefono = request.POST['telefono']
        usuario.habilitado = Habilitado.objects.get(id=request.POST['habilitado'])
        usuario.perfil = Perfil.objects.get(id=request.POST['perfil'])
        usuario.cargo = Cargo.objects.get(id=request.POST['cargo'])

        usuario.save()
        return render(request,"cliente/dashboard_usuarios.html",{'usuarios':Usuario.objects.all(),'datos':usuario})
    login = Usuario.objects.get(documento=request.session.get('user'))
    persona = Usuario.objects.get(documento=id)
    habilitado = Habilitado.objects.all()
    perfil = Perfil.objects.all()
    cargo = Cargo.objects.all()
    return render(request,'cliente/actualizar_usuario.html',{'login':login,'persona':persona,'hab':habilitado,'perfil':perfil,'cargo':cargo})

def deshabilitar(request, documento):
     usuario = Usuario.objects.get(documento=documento)
     usuario.habilitado = Habilitado.objects.get(id=2)
     usuario.save()
     informacion = {
                    'datos':usuario,
                    'usuarios':Usuario.objects.all()
                               }
     return render(request,'cliente/dashboard_usuarios.html',informacion)

def habilitar(request, documento):
     usuario = Usuario.objects.get(documento=documento)
     usuario.habilitado = Habilitado.objects.get(id=1)
     usuario.save()
     informacion = {
                    'datos':usuario,
                    'usuarios':Usuario.objects.all()
                               }
     return render(request,'cliente/dashboard_usuarios.html',informacion)