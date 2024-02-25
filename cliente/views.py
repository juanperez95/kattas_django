from django.shortcuts import render

def loginView(request):
    return render(request, "cliente/login.html")

def indexView(request):
    return render(request, "cliente/index.html")

def registroView(request):
    return render(request, "cliente/registro.html")

def dashboard_base(request):
    return render(request,"cliente/dashboard.html")

def dashboard_insumos(request):
    return render(request,"cliente/dashboard_insumo.html")

def dashboard_usuarios(request):
    return render(request,"cliente/dashboard_usuarios.html")

def dashboard_productos(request):
    return render(request,"cliente/dashboard_productos.html")
    
