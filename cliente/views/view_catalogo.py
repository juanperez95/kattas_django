from django.shortcuts import render, redirect
from ..models import *
from django.core.paginator import Paginator


global productos
productos = {}


def indexView(request):
    return render(request, ("cliente/index.html"))

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
        if int(request.POST['cantidad']) >= 0: # Validar que no se agreguen valores en cero.
            productos[producto.id]=[producto,int(request.POST['cantidad']),producto.precio*int(request.POST['cantidad'])]
            data['n_productos'] = len(productos)
    return render(request,'cliente/catalogo_productos.html',data)


def carrito(request):
    producto = [(k,v) for k,v in productos.items()]
    paginacion = Paginator(producto,4)
    pagina = request.GET.get('pagina')
    paginador = paginacion.get_page(pagina)
    return render(request,"cliente/carrito.html",{'carrito':paginador})

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

