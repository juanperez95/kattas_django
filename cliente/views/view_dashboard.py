from datetime import date, datetime
import os
from django.shortcuts import render, redirect
from django.conf import settings
from cliente.models import *
from django.core.paginator import Paginator
from django.db.models import Q


def dashboard_base(request):
    return render(request,"cliente/dashboard.html")

def dashboard_insumos(request):
    data={}
    usuario = Usuario.objects.get(documento=request.session.get('user'))
    categorias = Categoria.objects.all()
    insumos=Insumo.objects.all()
    data['datos']=usuario
    data['categorias']=categorias    
    paginacion = Paginator(insumos,8)
    pagina = request.GET.get('pagina')
    paginador = paginacion.get_page(pagina)
    data['entidad']=paginador
    return render(request,"cliente/dashboard_insumo.html",data)

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
    login = Usuario.objects.get(documento=request.session.get('user'))
    paginacion = Paginator(Producto.objects.all(),8)
    pagina = request.GET.get('pagina')
    paginador = paginacion.get_page(pagina)
    data={
        'datos':login,
        'entidad':paginador
        }
    return render(request,"cliente/dashboard_productos.html",data)
    
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

def registrar_insumo(request):
    if request.method=="POST":
        nombre_insumo=request.POST['n_insumo']
        c_minima=request.POST['c_minima']
        categoriaInsumo=request.POST['categoria']
        insumo=Insumo(
            nombre_insumo=nombre_insumo,
            cantidad_existente=0,
            cantidad_minimo=c_minima,
            fk_categoria=Categoria.objects.get(id=categoriaInsumo),
            fk_estado=Estado.objects.get(id=3)          
        )
        insumo.save()
    return redirect('dashboard_insumo')




def entrada_insumo(request, id):
    login = Usuario.objects.get(documento=request.session.get('user'))
    insumo=Insumo.objects.get(id=id)
    now = datetime.now()
    formato = now.strftime('%d/%m/%Y')

    data={
        'datos':login,
        'f_actual':formato,
        'insumo':insumo       
    }
    if request.method == 'POST':
        c_entrada=request.POST['c_entrada']
        f_vencimiento=request.POST['f_vencimiento']
        entrada_insumo=Entrada_Insumo(
            cantidad_entrada=c_entrada,
            fecha_vencimiento=f_vencimiento,
            fk_insumo=insumo,
            estado_vencido="Vigente"           
        )
        entrada_insumo.save()
        insumo.cantidad_existente += int(c_entrada)
        insumo.save()
        if insumo.cantidad_existente > insumo.cantidad_minimo:
            insumo.fk_estado=Estado.objects.get(id=1)
        elif insumo.cantidad_existente < insumo.cantidad_minimo:
            insumo.fk_estado=Estado.objects.get(id=2)
        elif insumo.cantidad_existente == 0:
            insumo.fk_estado=Estado.objects.get(id=3)            
        insumo.save()
        return redirect('dashboard_insumo')
    
    
    
    return render(request,'cliente/entrada_insumo.html',data)

def dashboard_entrada(request,id):
    login = Usuario.objects.get(documento=request.session.get('user'))    
    insumo=Insumo.objects.get(id=id)
    entradas= Entrada_Insumo.objects.filter(fk_insumo=insumo)
    if request.method == "POST":
        if request.POST.get('id_entrada'):
            entradas = Entrada_Insumo.objects.filter(id__icontains=request.POST.get('id_entrada'),fk_insumo=insumo)
        
        elif request.POST.get('f_vencimiento'):
            entradas = Entrada_Insumo.objects.filter(fecha_vencimiento=request.POST.get('f_vencimiento'),fk_insumo=insumo)

            
        elif request.POST.get('f_entrada'):
            entradas = Entrada_Insumo.objects.filter(fecha_entrada=request.POST.get('f_entrada'),fk_insumo=insumo)

            
        elif request.POST.get('estado_vencido'):
            entradas = Entrada_Insumo.objects.filter(estado_vencido=request.POST.get('estado_vencido'),fk_insumo=insumo)
    
    paginacion = Paginator(entradas,8)
    pagina = request.GET.get('pagina')
    paginador = paginacion.get_page(pagina)
    data={
        'datos':login,
        'entidad':paginador,
    }
    

    return render(request, 'cliente/dashboard_entrada.html',data)

# ----------------------------------------------------------------- productos-----------------------------------------------------------------
def registrar_productos(request):
    if request.method == "POST":
        nombre_producto = request.POST['n_producto']
        descripcion = request.POST['descripcion']
        tamano = request.POST['tamano']
        precio = request.POST['precio']
        imagen = request.FILES['archivo']
        print(imagen.name)
        with open(os.path.join(settings.MEDIA_ROOT,imagen.name),"wb") as archivo:
            for megas in imagen.chunks():
                archivo.write(megas)

        producto = Producto(
                fk_estado=Estado.objects.get(id=3),
                nombre_producto=nombre_producto,
                descripcion=descripcion,
                tamaño=tamano,
                precio=precio
            )
        producto.save()
        return redirect('dashboard_productos')
    return render(request,"cliente/registrar_producto.html",{'datos':request.session.get('user')})
    