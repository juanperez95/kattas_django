# from django.shortcuts import render
import base64
from cliente.models import *
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
# from weasyprint import HTML
from xhtml2pdf import pisa
from io import BytesIO
import os
import datetime

# def reporte_pdf(request):
#     # Obtener todos los usuarios registrados
#     usuarios = Usuario.objects.all()
    
#     # Pasar los datos al template
#     datos_reporte = {
#         'titulo': 'Reporte de Usuarios Registrados',
#         'usuarios': usuarios,
#     }
    
#     # Renderizar el template HTML
#     template = get_template('cliente/pdf_dashboard.html')
#     html_content = template.render(datos_reporte)
    
#     # Generar el PDF usando WeasyPrint
#     pdf_file = HTML(string=html_content).write_pdf()
    
#     # Devolver el PDF como una respuesta HTTP
#     response = HttpResponse(pdf_file, content_type='application/pdf')
#     response['Content-Disposition'] = 'filename="reporte.pdf"'
#     return response


def generar_pdf(request):
    if request.method == "POST":
        print("entra a la condicion")
        total = 0
        pedidos = Pedido.objects.filter(fecha_pedido__range=(request.POST['f_inicial'],request.POST['f_fin']),fk_estado=Estado_Pedido.objects.get(id=request.POST['estado']))
        for pedido in pedidos:
            total += pedido.total
            
        fecha_actual= datetime.datetime.now()

        data={
            'pedidos':pedidos,
            'total':total,    
            'f_inicial':request.POST['f_inicial'],
            'f_final':request.POST['f_fin'], 
            'fecha_actual': fecha_actual     
            }
        template = get_template("cliente/pdf_dashboard.html")
        html = template.render(data)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
        if not pdf.err:
            print("Se genera")
            # resultado =  
            return HttpResponse(result.getvalue(), content_type='application/pdf')
            # resultado['Content-Disposition'] = f"attachment; filename={fecha_actual}.pdf"
            # return resultado
    return None
    
    


