from datetime import date, datetime
from django.utils import timezone
import os
from django.shortcuts import render, redirect
from django.conf import settings
from cliente.models import *
from django.core.paginator import Paginator
import hashlib as h
from django.template.loader import render_to_string
from django.core.mail import send_mail,EmailMultiAlternatives

# Paginacion para cada tabla
# Recuperar sesion del usuario logueado
from .view_catalogo import sesion, paginacion, generar_venta


# Insumos para productos
global datos_insumo
datos_insumo = {}


def limpiar_lista(request):
    datos_insumo.clear()
    return redirect('registrar_producto')

def borrar_insumo_p(request,key):
    datos_insumo.pop(key)
    return redirect('registrar_producto')

def agregar_insumo_p(request):
    datos_insumo[request.POST['n_insumo']] = request.POST['c_insumo']
    return redirect('registrar_producto')

def dashboard_base(request):
    if request.session.get('user') is None:
        return redirect('login')
    return render(request,"cliente/dashboard.html")

def dashboard_insumos(request,m={}):
    if request.session.get('user') is None:
        return redirect('login')
    data={
        'n_insumos':Insumo.objects.count(),
        'n_disponibles':len(Insumo.objects.filter(fk_estado=Estado.objects.get(id=1))),
        'n_vencido':len(Entrada_Insumo.objects.filter(estado_vencido="Vencido")),
        'notificacion':m,
        }
    categorias = Categoria.objects.all()
    data['datos']=sesion(request)
    data['categorias']=categorias    
    data['entidad']=paginacion(request,Insumo.objects.all(),6)
    return render(request,"cliente/dashboard_insumo.html",data)

def dashboard_usuarios(request,m={}):
    if request.session.get('user') is None:
        return redirect('login')
    usuarios = Usuario.objects.all()
    if request.method == "POST":
        usuarios = Usuario.objects.filter(documento__icontains=request.POST['documento'])
    data={
        'entidad':paginacion(request,usuarios,7),
        'datos':sesion(request),
        'n_usuarios':Usuario.objects.count(),
        'n_deshabilitados':len(Usuario.objects.filter(habilitado=Habilitado.objects.get(id=2))),
        'n_clientes':len(Usuario.objects.filter(perfil=Perfil.objects.get(id=3))),
        'n_empleados':len(Usuario.objects.filter(perfil=Perfil.objects.get(id=2))),
        'notificacion':m,
        }
    
    return render(request,"cliente/dashboard_usuarios.html",data)

def dashboard_productos(request,datos={}):
    if request.session.get('user') is None:
        return redirect('login')
    data={
        'datos':sesion(request),
        'entidad':paginacion(request,Producto.objects.all(),7),
        'n_productos':Producto.objects.count(),
        'n_disponibles':len(Producto.objects.filter(fk_estado=Estado.objects.get(id=1))),
        'notificacion':datos,
        }
    return render(request,"cliente/dashboard_productos.html",data)
    
def actualizar_usuario(request, id):
    if request.session.get('user') is None:
        return redirect('login')
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
        data={
            'mensaje':f'¡Usuario {usuario.documento} ha sido actualizado!',
            'icono':'success',
            'title':'¡Actualizado!'
        }
        request.method = ""
        return dashboard_usuarios(request,data)  
    persona = Usuario.objects.get(documento=id)
    habilitado = Habilitado.objects.all()
    perfil = Perfil.objects.all()
    cargo = Cargo.objects.all()
    return render(request,'cliente/actualizar_usuario.html',{'datos':sesion(request),'persona':persona,'hab':habilitado,'perfil':perfil,'cargo':cargo})
    

def deshabilitar(request, documento):
    data={
        'icono':'success',
        'title':"¡Deshabilitado!"
    }
    usuario_d = Usuario.objects.get(documento=documento)
    usuario_d.habilitado = Habilitado.objects.get(id=2)
    usuario_d.save()
    return dashboard_usuarios(request,data)  


def habilitar(request, documento):
    data={
        'icono':'success',
        'title':"¡Habilitado!"
    }
    usuario_h = Usuario.objects.get(documento=documento)
    usuario_h.habilitado = Habilitado.objects.get(id=1)
    usuario_h.save()
    return dashboard_usuarios(request,data)   

def registrar_insumo(request):
    data={}
    if request.method=="POST":
        try:
            nombre_insumo=request.POST['n_insumo'].capitalize()
            if nombre_insumo != "": # Si el insumo no tiene nombre
                Insumo.objects.get(nombre_insumo=nombre_insumo) # Validar la existencia del insumo
                data['mensaje'] = f"¡Insumo {nombre_insumo} ya esta registrado!"
                data['icono'] = "error"
            else:
                data['mensaje'] = f"¡Nombre de insumo no valido!"
                data['icono'] = "error"
        except Exception as err: # Si existe el insumo no se registra
            
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
            data['mensaje'] = f"¡Insumo {nombre_insumo} ha sido creado exitosamente!"
            data['icono'] = "success"
    return dashboard_insumos(request,data)




def entrada_insumo(request, id):
    if request.session.get('user') is None:
        return redirect('login')
    insumo=Insumo.objects.get(id=id)
    now = datetime.now()
    formato = now.strftime('%d/%m/%Y')

    data={
        'datos':sesion(request),
        'f_actual':formato,
        'insumo':insumo       
    }
    if request.method == 'POST':
        c_entrada=int(request.POST['c_entrada'])
        if not c_entrada < 0: # Si no es negativo el valor procede a crear la entrada
            f_vencimiento=request.POST['f_vencimiento']
            entrada_insumo=Entrada_Insumo(
                cantidad_entrada=c_entrada,
                cantidad_inicial=c_entrada,
                fecha_vencimiento=f_vencimiento,
                fk_insumo=insumo,
                estado_vencido="Vigente"           
            )
            entrada_insumo.save()
            insumo.cantidad_existente += int(c_entrada)
            insumo.save()
            data['mensaje'] = "¡Entrada creada exitosamente!"
            data['icono'] = "success"
            
            if insumo.cantidad_existente > insumo.cantidad_minimo:
                insumo.fk_estado=Estado.objects.get(id=1)
            elif insumo.cantidad_existente < insumo.cantidad_minimo:
                insumo.fk_estado=Estado.objects.get(id=2)
                
                
            if insumo.cantidad_existente == 0:
                insumo.fk_estado=Estado.objects.get(id=3)    
                    
                
                
            insumo.save()

        return dashboard_insumos(request,data)
    
    
    
    return render(request,'cliente/entrada_insumo.html',data)

def dashboard_entrada(request,ids):
    if request.session.get('user') is None:
        return redirect('login')  
    insumo=Insumo.objects.get(id=ids)
    entradas= Entrada_Insumo.objects.filter(fk_insumo=insumo).order_by("-id")
    for entrada in entradas:
        # fecha_actual = timezone.now().date()
        if entrada.fecha_vencimiento < timezone.now().replace(hour=0, minute=0, second=0, microsecond=0):
            entrada.estado_vencido = "Vencido"
            entrada.save()

        
    if request.method == "POST":
       
        if request.POST.get('f_vencimiento'):
            entradas = Entrada_Insumo.objects.filter(fecha_vencimiento=request.POST.get('f_vencimiento'),fk_insumo=insumo)

            
        elif request.POST.get('f_entrada'):
            entradas = Entrada_Insumo.objects.filter(fecha_entrada=request.POST.get('f_entrada'),fk_insumo=insumo)

            
        elif request.POST.get('estado_vencido'):
            entradas = Entrada_Insumo.objects.filter(estado_vencido=request.POST.get('estado_vencido'),fk_insumo=insumo)
    data={
        'datos':sesion(request),
        'entidad':paginacion(request,entradas,8),
    }
    

    return render(request, 'cliente/dashboard_entrada.html',data)

# ----------------------------------------------------------------- productos-----------------------------------------------------------------
def registrar_productos(request):
    ob_insumos= [(k,v) for k, v in datos_insumo.items()] # Diccionario de insumos
    data = {
        'datos':Usuario.objects.get(documento=request.session.get('user')),
        'insumos':Insumo.objects.all(),
        'insumos_productos':paginacion(request,ob_insumos,3)
        }
    if request.method == "POST":
        nombre_producto = request.POST['n_producto'].capitalize()
        descripcion = request.POST['descripcion'].capitalize()
        tamano = request.POST['tamano']
        precio = request.POST['precio']
        imagen = request.FILES['archivo']

        producto = Producto(
                fk_estado=Estado.objects.get(id=3),
                nombre_producto=nombre_producto,
                descripcion=descripcion,
                tamaño=tamano,
                precio=precio,
                foto_p=imagen
            )
        producto.save()
        # Buscar producto
        producto = Producto.objects.get(nombre_producto=nombre_producto)

        # Iterar el diccionario
        for insumos_p, cantidad in datos_insumo.items():

            prod_ins = Producto_Insumo(
                insumos=Insumo.objects.get(nombre_insumo=insumos_p),
                productos=producto,
                cantidad=cantidad
                )
            prod_ins.save()

        # Actualzar estado del producto
            
        producto_insumo = Producto_Insumo.objects.filter(productos=producto)

        for cantidades_insumo in producto_insumo:
            if cantidades_insumo.cantidad == 0:
                producto.fk_estado = Estado.objects.get(id=3)
                break
            else:
                producto.fk_estado = Estado.objects.get(id=1)

        producto.save()
        data['title']="¡Producto creado!"
        data['icono']="success"
        data['mensaje']=f"¡El producto {producto.nombre_producto} ha sido creado correctamente!"
        datos_insumo.clear()

        return dashboard_productos(request,data)
    return render(request,"cliente/registrar_producto.html",data)

def insumos_productos(request,id_producto,id_p_i):
    data={
        'entidad':paginacion(request,Producto_Insumo.objects.filter(productos=Producto.objects.get(id=id_producto)),8),
        'datos':sesion(request),
        'producto':Producto.objects.get(id=id_producto)
        }
    try:
        producto_insumo = Producto_Insumo.objects.get(id=id_p_i)
        data['id'] = producto_insumo
    except Exception as err:
        pass
    return render(request,"cliente/dashboard_insumo_producto.html",data)




def editar_insumo_producto(request,id):
    p_i = Producto_Insumo.objects.get(id=id)
    p_i.cantidad = request.POST['cantidad']
    p_i.save()
    return redirect("insumos_productos",p_i.productos.id,0)
# ------------------------------------------------------------------------- Pedidos ---------------------------------------------------
def dashboard_pedidos(request,m={}):
    
    data = {
        'entidad': paginacion(request,Pedido.objects.all(),8),
        'datos':sesion(request),
        'estados':Estado_Pedido.objects.all(),
        'notificacion':m,
        }    
    if request.method == "POST":
        try:
            data['entidad'] = paginacion(request,Pedido.objects.filter(id=int(request.POST['filtro_pedido'])),8)
        except Exception as err:
            pass

    return render(request,"cliente/dashboard_pedido.html",data)

def dashboard_pedido_producto(request,id):
    data={
        'entidad':paginacion(request,Pedido_Producto.objects.filter(fk_pedido=Pedido.objects.get(id=id)),8),
        'datos':sesion(request)
        }
    return render(request,"cliente/dashboard_producto_pedido.html",data)

def actualizar_estado_pedido(request,id):
    data = {
        'entidad': paginacion(request,Pedido.objects.filter(id=id),1),
        'datos':sesion(request),
        'estados':Estado_Pedido.objects.all(),
        'id':Pedido.objects.get(id=id)
        }    
    
    if request.method == "POST":
        pedido = Pedido.objects.get(id=id)
        pedido.fk_estado = Estado_Pedido.objects.get(id=request.POST['estado_pedido'])
        pedido.save()
        data['title'] = "¡Estado actualizado!"
        data['icono'] = "success"
        data['mensaje'] = f"¡El estado del pedido {pedido.id} es {pedido.fk_estado.tipo_estado}!"
        if pedido.fk_estado.id == 1:
            # Genera venta
            enviar_factura(request,pedido)
            return generar_venta(request,pedido.id)
        
        return dashboard_pedidos(request,data)
    return render(request,f'cliente/dashboard_pedido.html',data)

# ----------------------------------------------------- Dashboard cliente--------------------------------------------
def mis_pedidos(request,datos={}):
    data={
        'datos':sesion(request),
        'entidad':paginacion(request,Pedido.objects.filter(fk_documento=sesion(request)),8),
        'notificacion':datos,
        }
    if request.method == "POST":
        try:
            data['entidad'] = paginacion(request,Pedido.objects.filter(id=int(request.POST['filtro_pedido'])),1)
        except Exception as err:
            pass


    return render(request,"cliente/dashboard_mis_pedidos.html",data)


# Editar usuarios ----------------------------------------------------------------------------------



def editarUsuario(request,datos={}):
    usuario = sesion(request)
    data={
        'datos':sesion(request),
        'notificacion':datos,
        }
    
    if request.method == "POST":
        usuario.apellidos=request.POST['apellido']
        usuario.nombre=request.POST['Nombre']
        usuario.email=request.POST['email']
        usuario.telefono=request.POST['telefono']
        usuario.direccion=request.POST['direccion']
        try:
            usuario.foto_perfil=request.FILES['foto_perfil']
        except Exception as err:
            pass
        data['title'] = "¡Actualizado!"
        data['icono'] = "success"
        data['mensaje'] = f"Usuario {usuario.nombre} ha sido actualizado."
        usuario.save()
        request.method = ''
        return mis_pedidos(request,data)
    return render(request,'cliente/editarUsuario.html',data)

def cambiar_password(request):
    data={}
    if request.method == "POST":
        usuario = sesion(request)
        encriptada = h.sha1(request.POST['actual'].encode()).hexdigest()
        if usuario.password == encriptada:
            usuario.password = h.sha1(request.POST['nueva'].encode()).hexdigest()
            usuario.save()
            data['title']="Cambio exitoso"
            data['icono']="success"
            data['mensaje']="¡Tu contraseña ha sido actualizada!"
            request.method = ''
            return mis_pedidos(request,data)
        data['title']="¡Ups!"
        data['icono']="error"
        data['mensaje']="¡La contraseña actual no es correcta!"
        request.method = ''
        return editarUsuario(request,data)

def enviar_factura(request,pedido=None):

    data={
        'items':Pedido_Producto.objects.filter(fk_pedido=pedido),
        'pedido': pedido
        }
    html = render_to_string("cliente/factura.html",data)
    asunto = f"Factura pedido n° {pedido.id}"

    correo = Usuario.objects.get(documento=pedido.fk_documento.documento)
    msg = EmailMultiAlternatives(
                subject=asunto,
                body="",
                from_email="jplesmes19@gmail.com",
                to=[correo.email]
            )
    msg.attach_alternative(html, "text/html")
    msg.send()

    return redirect('inicio')


