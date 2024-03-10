# from django.shortcuts import render
# from cliente.models import Usuario,Perfil,Habilitado,Cargo
# from django.http import HttpResponse
# from django.template.loader import get_template
# from weasyprint import HTML

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
