from django.shortcuts import render, redirect
from cliente.models import Usuario,Perfil,Habilitado,Cargo
import hashlib as h
from django.core.mail import send_mail,EmailMultiAlternatives
import random as r


def html_correo(titulo,asunto, contenido, correo):
    html_content = """
        <html>
        <head>
            <style>
                /* Definición de estilos CSS */
                body {font-family: Arial, sans-serif;
                    background-color: #f0f0f0;
                }
                h1 {
                    color: #333;
                }
                p {
                    font-size: 16px;
                    color: #666;
                }
            </style>
        </head>
        <body> 
            <img src='https://i.postimg.cc/GhrDCHvp/Logokatta-s-sin-fondo.png' / style="float: left; width: 300px;">
            <h1>"""+titulo+"""</h1>
            <p>"""+str(contenido)+"""</p>
        </body>
        </html>
        """
    msg = EmailMultiAlternatives(
                subject=asunto,
                body="",
                from_email="jplesmes19@gmail.com",
                to=[correo]
            )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def loginView(request):
    data = {'mensaje':10}
    if request.method == "POST":
        password = h.sha1(request.POST['clave'].encode()).hexdigest() # Encriptar clave
        try:
            # Validar si la contraseña coincide, esta habilitado y es administrador o empleado
            usuario = Usuario.objects.get(
                documento=int(request.POST['documento']),
                password=password
                )
            # Validar si esta habilitado o no
            if usuario.habilitado.id == 1:
                # Crear la sesion del usuario
                request.session['user'] = usuario.documento
                if usuario.perfil.id == 1 or usuario.perfil.id == 2:
                    return redirect('dashboard_usuarios')
                else:
                    return redirect('inicio') # Si es cliente
                
            data['mensaje'] = f"¡El usuario {usuario.nombre} no esta habilitado!"
            data['title'] = "¡Ups!"
            data['icono'] = "error"
        except Exception as err:
            data['mensaje'] = "Oops, ¡Credenciales incorrectos!"
            data['title'] = "¡Ups!"
            data['icono'] = "error"
            
    return render(request, "cliente/login.html",data)

def indexView(request):
    return render(request, "cliente/index.html")

def recuperar_pass(request):
    if request.method == "POST":
        data = {'m':0}
        correo = request.POST['email']
        codigo_generado = r.randint(1000,9999) # Generar contraseña por el sistema de 4 digitos
        mensaje = f"Su contraseña es {codigo_generado} para ingresar a la plataforma"
        try:
            usuario = Usuario.objects.get(email=correo)
            html_correo("Recuperar contraseña Kattas WEB","Recuperar Contraseña",mensaje,correo)
            encryptada = h.sha1(str(codigo_generado).encode()).hexdigest()
            usuario.password = encryptada
            usuario.save()
            
        except Exception as err:
            data['m'] = 1
            pass

        return render(request,"cliente/recuperarContraseña.html",data)
    return render(request,"cliente/recuperarContraseña.html")


# Registro usuarios
def registroView(request):
    data={}
    if request.method == "POST":
        # Validar la existencia del documento
        try:
            usuario = Usuario.objects.get(documento=request.POST['documento'])
            if usuario != None:
                return render(request,"cliente/registro.html",{'mensaje':3})
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
                cargo=Cargo.objects.get(id=4),
                password=password,
                nombre=nombre,
                apellidos=apellido,
                email=correo,
                fecha_nacimiento=f_nacimiento,
                genero=genero,
                telefono=telefono,
                direccion=direccion
            )
            message = "Gracias por formar parte de nuestra comunidad."
            html_correo("¡Bienvenido!","Registro Exitoso",message,correo)
            usuario.save()
            data['mensaje'] = "¡Registro exitoso!"
            data['title'] = "¡Hurra!"
            data['icono'] = "success"
        return render(request,'cliente/login.html',data)
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


    
