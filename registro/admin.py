from django.contrib import admin

from .models import Estudiante


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ("cedula", "nombre_completo", "correo", "edad", "carrera")
    list_filter = ("carrera", "fecha_registro")
    search_fields = ("cedula", "nombre", "apellido", "correo")
    readonly_fields = ("fecha_registro", "fecha_actualizacion")
    ordering = ("apellido", "nombre")
    date_hierarchy = "fecha_registro"

    @admin.display(description="Nombre", ordering="apellido")
    def nombre_completo(self, estudiante):
        return f"{estudiante.nombre} {estudiante.apellido}"
