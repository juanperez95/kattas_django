from django.urls import path
from .views import view_dashboard, view_catalogo, view_login

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
    

]