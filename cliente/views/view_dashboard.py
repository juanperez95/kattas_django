from django.shortcuts import render, redirect
from cliente.models import *
from django.core.paginator import Paginator


def dashboard_base(request):
    return render(request,"cliente/dashboard.html")

def dashboard_insumos(request):
    usuario = Usuario.objects.get(documento=request.session.get('user'))
    return render(request,"cliente/dashboard_insumo.html",{'datos':usuario})

def dashboard_usuarios(request):
    usuarios = Usuario.objects.all()
    if request.method == "POST":
        usuarios = Usuario.objects.filter(documento__icontains=request.POST['documento'])
    usuario =  Usuario.objects.get(documento=request.session.get('user'))
    paginacion = Paginator(usuarios,8)
    pagina = request.GET.get('pagina')
    paginador = paginacion.get_page(pagina)
    return render(request,"cliente/dashboard_usuarios.html",{'entidad':paginador,'datos':usuario})

def dashboard_productos(request):
    return render(request,"cliente/dashboard_productos.html")
    
def actualizar_usuario(request, id):
    login = Usuario.objects.get(documento=request.session.get('user'))
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
        return redirect('dashboard_usuarios')    
    persona = Usuario.objects.get(documento=id)
    habilitado = Habilitado.objects.all()
    perfil = Perfil.objects.all()
    cargo = Cargo.objects.all()
    return render(request,'cliente/actualizar_usuario.html',{'datos':login,'persona':persona,'hab':habilitado,'perfil':perfil,'cargo':cargo})
    

def deshabilitar(request, documento):
    usuario_d = Usuario.objects.get(documento=documento)
    usuario_d.habilitado = Habilitado.objects.get(id=2)
    usuario_d.save()
    return redirect('dashboard_usuarios')    


def habilitar(request, documento):
    usuario_h = Usuario.objects.get(documento=documento)
    usuario_h.habilitado = Habilitado.objects.get(id=1)
    usuario_h.save()
    return redirect('dashboard_usuarios')    
