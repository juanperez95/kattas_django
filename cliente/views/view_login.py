from django.shortcuts import render, redirect
from ..models import Usuario,Perfil,Habilitado,Cargo
import hashlib as h

def loginView(request):
    data = {'mensaje':0}
    if request.method == "POST":
        try:
            usuario = Usuario.objects.get(documento=int(request.POST['documento']))
            password = h.sha1(request.POST['clave'].encode()).hexdigest() # Encriptar clave
            # Validar si la contraseña coincide, esta habilitado y es administrador o empleado
            if password == usuario.password and usuario.habilitado.id == 1 and usuario.perfil.id == 1 or usuario.perfil.id == 2:
                request.session['user'] = str(usuario.documento) # Crear session
                informacion = {
                    'datos':usuario,
                    'usuarios':Usuario.objects.all()
                               }
                return render(request,"cliente/dashboard_usuarios.html",informacion)
            elif password == usuario.password and usuario.habilitado.id == 1 and usuario.perfil.id == 3:
                informacion = {
                    'datos':usuario
                    }
                return render(request,"cliente/dashboard_usuarios.html",informacion)
            elif password == usuario.password and usuario.habilitado.id == 2:
                data['mensaje'] = 2
                return render(request,"cliente/login.html",data)
            elif password != usuario.password and usuario.habilitado.id == 1:
                data['mensaje'] = 0
                return render(request,"cliente/login.html",data)
        except Exception as err:
            data['mensaje'] = 1
        return render(request,"cliente/login.html",data)
            
    return render(request, "cliente/login.html")

def indexView(request):
    return render(request, "cliente/index.html")

# Registro usuarios
def registroView(request):
    if request.method == "POST":
        # Validar la existencia del documento
        try:
            usuario = Usuario.objects.get(documento=request.POST['documento'])
            if usuario != None:
                return render(request,"cliente/registro.html",{'mensaje':0})
        except Exception as err:  # Si no llega a encontrar el documento procede con el registro
            documento = request.POST['documento']
            nombre = request.POST['nombres']
            apellido = request.POST['apellidos']
            f_nacimiento = request.POST['f_nacimiento']
            direccion = request.POST['direccion']
            telefono = request.POST['telefono']
            correo = request.POST['correo']
            password = h.sha1(request.POST['pass'].encode()).hexdigest()
            genero = request.POST['genero']
            usuario = Usuario(
                documento=documento,
                habilitado=Habilitado.objects.get(id=1),
                perfil=Perfil.objects.get(id=3),
                cargo=Cargo.objects.get(id=3),
                password=password,
                nombre=nombre,
                apellidos=apellido,
                email=correo,
                fecha_nacimiento=f_nacimiento,
                genero=genero,
                telefono=telefono,
                direccion=direccion
            )
            usuario.save()
        return redirect('login')
    return render(request,'cliente/registro.html')
# Cierre sesion
def cerrar_sesion(request):
    try:
        if request.session['user']:
            del request.session['user'] # Limpiar la sesion
            return redirect('login')
    except KeyError: # Si no llega a encontrar la clave
        pass
    return redirect('inicio')
    
