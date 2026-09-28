from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from .excel import ErrorImportacionExcel, crear_excel_estudiantes, importar_estudiantes
from .forms import EstudianteForm, EstudianteUpdateForm, ImportarEstudiantesForm
from .models import Estudiante


@login_required
@permission_required("registro.add_estudiante", raise_exception=True)
@require_http_methods(["GET", "POST"])
def registrar(request):
    form = EstudianteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        estudiante = form.save()
        messages.success(request, "El estudiante fue registrado correctamente.")
        return redirect("registro:detalle", pk=estudiante.pk)
    return render(
        request,
        "registro/registrar.html",
        {"form": form, "importar_form": ImportarEstudiantesForm()},
    )


@login_required
@permission_required("registro.add_estudiante", raise_exception=True)
@require_POST
def importar_excel(request):
    importar_form = ImportarEstudiantesForm(request.POST, request.FILES)
    if importar_form.is_valid():
        try:
            cantidad = importar_estudiantes(importar_form.cleaned_data["archivo"])
        except ErrorImportacionExcel as exc:
            for error in exc.messages:
                importar_form.add_error("archivo", error)
        else:
            messages.success(request, f"Se importaron {cantidad} estudiantes correctamente.")
            return redirect("registro:lista")
    return render(
        request,
        "registro/registrar.html",
        {"form": EstudianteForm(), "importar_form": importar_form},
        status=400,
    )


@login_required
@permission_required("registro.view_estudiante", raise_exception=True)
def exportar_excel(request):
    contenido = crear_excel_estudiantes(Estudiante.objects.order_by("apellido", "nombre"))
    respuesta = HttpResponse(
        contenido,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    respuesta["Content-Disposition"] = 'attachment; filename="estudiantes.xlsx"'
    return respuesta


@login_required
@permission_required("registro.view_estudiante", raise_exception=True)
def lista(request):
    consulta = request.GET.get("q", "").strip()
    estudiantes = Estudiante.objects.all()
    if consulta:
        estudiantes = estudiantes.filter(
            Q(cedula__icontains=consulta)
            | Q(nombre__icontains=consulta)
            | Q(apellido__icontains=consulta)
            | Q(correo__icontains=consulta)
        )
    pagina = Paginator(estudiantes, 10).get_page(request.GET.get("page"))
    return render(
        request, "registro/lista.html", {"pagina": pagina, "consulta": consulta}
    )


@login_required
@permission_required("registro.view_estudiante", raise_exception=True)
def detalle(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    return render(request, "registro/detalle.html", {"estudiante": estudiante})


@login_required
@permission_required("registro.change_estudiante", raise_exception=True)
@require_http_methods(["GET", "POST"])
def editar(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    form = EstudianteUpdateForm(request.POST or None, instance=estudiante)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "La información fue actualizada correctamente.")
        return redirect("registro:detalle", pk=estudiante.pk)
    return render(
        request,
        "registro/editar.html",
        {"estudiante": estudiante, "form": form},
    )


@login_required
@permission_required("registro.delete_estudiante", raise_exception=True)
@require_POST
def eliminar(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    estudiante.delete()
    messages.success(request, "El estudiante fue eliminado correctamente.")
    return redirect("registro:lista")
