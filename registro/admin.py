from django.contrib import admin

from .models import Estudiante


admin.site.site_header = "Administración académica"
admin.site.site_title = "Gestión académica"
admin.site.index_title = "Panel de administración"


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ("cedula", "nombre_completo", "correo", "edad", "carrera")
    list_filter = ("carrera", "fecha_registro")
    search_fields = ("cedula", "nombre", "apellido", "correo")
    readonly_fields = ("fecha_registro", "fecha_actualizacion")
    ordering = ("apellido", "nombre")
    date_hierarchy = "fecha_registro"
    list_per_page = 20
    fieldsets = (
        (
            "Identificación",
            {"fields": (("cedula", "edad"), ("nombre", "apellido"))},
        ),
        ("Información académica", {"fields": ("correo", "carrera")}),
        (
            "Fechas del sistema",
            {
                "fields": (("fecha_registro", "fecha_actualizacion"),),
                "classes": ("collapse",),
            },
        ),
    )

    @admin.display(description="Nombre", ordering="apellido")
    def nombre_completo(self, estudiante):
        return f"{estudiante.nombre} {estudiante.apellido}"
