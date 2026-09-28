from django.urls import path

from . import views

app_name = "registro"

urlpatterns = [
    path("", views.lista, name="lista"),
    path("estudiantes/nuevo/", views.registrar, name="registrar"),
    path("estudiantes/importar-excel/", views.importar_excel, name="importar_excel"),
    path("estudiantes/exportar-excel/", views.exportar_excel, name="exportar_excel"),
    path("estudiantes/<int:pk>/", views.detalle, name="detalle"),
    path("estudiantes/<int:pk>/editar/", views.editar, name="editar"),
    path("estudiantes/<int:pk>/eliminar/", views.eliminar, name="eliminar"),
]
