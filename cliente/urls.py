from django.urls import path
from .views import *
urlpatterns = [
    path("login/", loginView,name="login"),
    path("", indexView,name="inicio"),
    path("registro/", registroView,name="registro_usuarios"),
    path("dashboard/", dashboard_base,name="dashboard_base"),
    path("insumo_admin/", dashboard_insumos,name="dashboard_insumo"),
    path("users_admin/", dashboard_usuarios,name="dashboard_usuarios"),
    path("productos_admin/", dashboard_productos,name="dashboard_productos"),
]