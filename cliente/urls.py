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
]