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
    data = {'mensaje':0}
    if request.method == "POST":
        try:
            usuario = Usuario.objects.get(documento=int(request.POST['documento']))
            password = h.sha1(request.POST['clave'].encode()).hexdigest() # Encriptar clave
            # Validar si la contraseña coincide, esta habilitado y es administrador o empleado
            if password == usuario.password and usuario.habilitado.id == 1 and usuario.perfil.id == 1 or usuario.perfil.id == 2: # Vista administradores
                request.session['user'] = str(usuario.documento) # Crear session
                return redirect('dashboard_usuarios')
            elif password == usuario.password and usuario.habilitado.id == 1 and usuario.perfil.id == 3: # Vista cliente

                return redirect('dashboard_usuarios')
            elif password == usuario.password and usuario.habilitado.id == 2:
                data['mensaje'] = 2
                return render(request,"cliente/login.html",data)
            elif password != usuario.password and usuario.habilitado.id == 1:
                data['mensaje'] = 0
                return render(request,"cliente/login.html",data)
            return redirect('dashboard_usuarios')
        except Exception as err:
            data['mensaje'] = 1
        return redirect('login')
            
    return render(request, "cliente/login.html")

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
            print(err)
            pass

        return render(request,"cliente/recuperarContraseña.html",data)
    return render(request,"cliente/recuperarContraseña.html")


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
                perfil=Perfil.objects.get(id=1),
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


    
