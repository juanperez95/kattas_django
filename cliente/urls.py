from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import view_dashboard, view_catalogo, view_login, view_pdf

urlpatterns = [
    # Registros, logueo e inicio de la pagina
    path("login/", view_login.loginView,name="login"),
    path("", view_catalogo.indexView,name="inicio"),
    path("registro/", view_login.registroView,name="registro_usuarios"),
    path("logout/", view_login.cerrar_sesion,name="cerrar_sesion"),
    # Dashboards de modulos
    path("dashboard/", view_dashboard.dashboard_base,name="dashboard_base"),
    path("insumo_admin/", view_dashboard.dashboard_insumos,name="dashboard_insumo"),
    path("users_admin/", view_dashboard.dashboard_usuarios,name="dashboard_usuarios"),
    path("productos_admin/", view_dashboard.dashboard_productos,name="dashboard_productos"),
    path('actualizar_usuario/<str:id>',view_dashboard.actualizar_usuario,name="actualizar_usuario"),
    path('deshabilitar_user/<str:documento>',view_dashboard.deshabilitar,name="deshabilitar_usuario"),
    path('habilitar_user/<str:documento>',view_dashboard.habilitar,name="habilitar_usuario"),
    path('recuperar_pass/',view_login.recuperar_pass,name="recuperar_pass"),
    #path('reporte/', view_pdf.reporte_pdf,name="pdf_dashboard"),
    path('registrar_insumo/',view_dashboard.registrar_insumo,name="registrar_insumo"),
    path('entrada_insumo/<str:id>',view_dashboard.entrada_insumo,name="entrada_insumo"),
    path('dashboard_entrada/<str:ids>',view_dashboard.dashboard_entrada,name="dashboard_entrada"),
    path('registrar_producto/',view_dashboard.registrar_productos,name="registrar_producto"),
    path('add_insumo_p/',view_dashboard.agregar_insumo_p,name="add_insumo_p"),
    path('del_insumo_p/<str:key>',view_dashboard.borrar_insumo_p,name="del_insumo_p"),
    path('limpiar/',view_dashboard.limpiar_lista,name="limpiar"),
    path('insumos_productos/<str:id_producto>/<str:id_p_i>',view_dashboard.insumos_productos,name="insumos_productos"),
    path('editar_insumo_producto/<str:id>',view_dashboard.editar_insumo_producto,name="editar_insumo_producto"),
    path('catalogo_productos/<str:id>',view_catalogo.catalogo_productos,name='catalogo_productos'),
    path('carrito/',view_catalogo.carrito,name='carrito'),
    path('borrar_carrito/<int:id>',view_catalogo.quitar_producto,name='borrar_carrito'),
    path('aumentar_carrito/<int:id>',view_catalogo.aumentar_cantidad_carrito,name='aumentar_carrito'),
    path('restar_carrito/<int:id>',view_catalogo.restar_cantidad_carrito,name='restar_carrito'),
    path('crear_pedido/<str:total>',view_catalogo.crear_pedido,name='crear_pedido'),
    path('dashboard_pedidos/',view_dashboard.dashboard_pedidos,name='dashboard_pedidos'),
    path('dashboard_pedidos_producto/<str:id>',view_dashboard.dashboard_pedido_producto,name='dashboard_pedidos_producto'),
    path('estado_pedido/<str:id>',view_dashboard.actualizar_estado_pedido,name='estado_pedido'),
    path('mis_pedidos/',view_dashboard.mis_pedidos,name='mis_pedidos'),
    path('configuracion/',view_dashboard.actualizar_estado_pedido,name='configuracion'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)