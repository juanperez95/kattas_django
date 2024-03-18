from django.shortcuts import render, redirect
from ..models import *
from django.core.paginator import Paginator


global productos,totales
totales=0
productos = {}


def paginacion(request,clase,cantidad):
    paginacion = Paginator(clase,cantidad)
    pagina = request.GET.get('pagina')
    paginador = paginacion.get_page(pagina)
    return paginador


def sesion(request):
    return Usuario.objects.get(documento=request.session['user'])

def indexView(request):
    data={}
    if request.session.get('user') is None:
        pass
    else:
        data['datos'] = Usuario.objects.get(documento=request.session.get('user'))
    return render(request, ("cliente/index.html"),data)

def catalogo_productos(request,id=0):
    producto=Producto.objects.all()
    paginacion = Paginator(producto,4)
    pagina = request.GET.get('pagina')
    paginador = paginacion.get_page(pagina)
    data={
            'entidad':paginador,
            'n_productos':len(productos),
        }
    try:
        
        p_catalogo=Producto.objects.get(id=id)
        data['p_catalogo']=p_catalogo
        
    except Exception as err:
        pass
    if request.method == "POST":        
        producto = Producto.objects.get(id=id)
        if int(request.POST['cantidad']) >= 1: # Validar que no se agreguen valores en cero.
            productos[producto.id]=[producto,int(request.POST['cantidad']),producto.precio*int(request.POST['cantidad'])]
            data['n_productos'] = len(productos)
    return render(request,'cliente/catalogo_productos.html',data)


def carrito(request):
    producto = [(k,v) for k,v in productos.items()]
    paginacion = Paginator(producto,4)
    pagina = request.GET.get('pagina')
    data={}
    totales=0
    paginador = paginacion.get_page(pagina)
    data['carrito']=paginador
    for total in productos.values():
            totales += total[2]
    data['total']=totales
    return render(request,"cliente/carrito.html",data)

def quitar_producto(request,id):
    productos.pop(id)
    return redirect("carrito")

def aumentar_cantidad_carrito(request,id):
    datos = productos[id]
    datos[1] = datos[1] + 1
    datos[2] = datos[1] * datos[0].precio
    return redirect("carrito")

def restar_cantidad_carrito(request,id):
    datos = productos[id]
    datos[1] = datos[1] - 1
    if datos[1] == 0:
        productos.pop(id)
    else:
        datos[2] = datos[1] * datos[0].precio
    return redirect("carrito")

def crear_pedido(request,total):


    if request.session.get('user') is None:
        return redirect('login')
    

    producto=Producto.objects.all()
    paginacion = Paginator(producto,4)
    pagina = request.GET.get('pagina')
    paginador = paginacion.get_page(pagina)
    data={
            'entidad':paginador,
            'n_productos':len(productos),
        }
    try:
        
        p_catalogo=Producto.objects.get(id=id)
        data['p_catalogo']=p_catalogo
        
    except Exception as err:
        pass

    if len(productos) == 0:
        data['notificacion'] = 1
        return render(request,'cliente/catalogo_productos.html',data)
    print(totales)
    pedido=Pedido(
        fk_documento=sesion(request),
        total=float(total),
        fk_estado=Estado_Pedido.objects.get(id=3)
        )
    pedido.save()
    for producto in productos.values():
        pedido_producto = Pedido_Producto(
                fk_pedido=pedido,
                fk_producto=producto[0],
                cantidad_producto=producto[1],
                precio_producto=producto[2]
            )
        pedido_producto.save()
    productos.clear()

    data['notificacion'] = 0
                
            
    return render(request,'cliente/catalogo_productos.html',data)
    

def generar_venta(request, id_pedido):
    # quitar de inventario ------------------------------------------------------------
    pedido = Pedido_Producto.objects.filter(id=id_pedido)
    for prod in pedido:    
        insumo_producto = Producto_Insumo.objects.filter(productos=prod.fk_producto)
        for ins in insumo_producto:
            insumo = Insumo.objects.get(id=ins.insumos.id)
            entrada_insumo = Entrada_Insumo.objects.filter(fk_insumo=ins)
            # ---- Descontar entrada ------------------------------------
            
            
            
            
            
            
            insumo.cantidad_existente -= (ins.cantidad*prod[1])
            if insumo.cantidad_existente >= 0:
                print("Se guardo")
                if insumo.cantidad_existente > insumo.cantidad_minimo:
                    insumo.fk_estado=Estado.objects.get(id=1)
                elif insumo.cantidad_existente < insumo.cantidad_minimo:
                    insumo.fk_estado=Estado.objects.get(id=2)
            
            
                if insumo.cantidad_existente == 0:
                    insumo.fk_estado=Estado.objects.get(id=3) 

                insumo.save()

                producto_insumo = Producto_Insumo.objects.filter(productos=prod[0])
                producto = prod[0]

                for cantidades_insumo in producto_insumo:
                    if cantidades_insumo.cantidad > cantidades_insumo.insumos.cantidad_existente:
                        producto.fk_estado = Estado.objects.get(id=3)
                        break
                    else:
                        producto.fk_estado = Estado.objects.get(id=1)

                producto.save()
    else:
                data['notificacion'] = 1
    pass