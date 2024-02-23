from django.shortcuts import render

def loginView(request):
    return render(request, "cliente/login.html")

def indexView(request):
    return render(request, "cliente/index.html")
def registroView(request):
    return render(request, "cliente/registro.html")
    
