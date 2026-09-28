from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.db.models.functions import Lower

from .validators import validar_cedula_ecuatoriana


class Estudiante(models.Model):
    """Representa a un estudiante registrado en la institución."""

    class Carrera(models.TextChoices):
        SOFTWARE = "SOF", "Software"
        ADMINISTRACION = "ADM", "Administración"
        DERECHO = "DER", "Derecho"
        OTRA = "OTR", "Otra"

    validador_nombre = RegexValidator(
        regex=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        message="Use únicamente letras, espacios, apóstrofes o guiones.",
    )

    cedula = models.CharField(
        "cédula", max_length=10, unique=True, validators=[validar_cedula_ecuatoriana]
    )
    nombre = models.CharField(max_length=100, validators=[validador_nombre])
    apellido = models.CharField(max_length=100, validators=[validador_nombre])
    correo = models.EmailField(unique=True)
    edad = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(16), MaxValueValidator(100)]
    )
    carrera = models.CharField(max_length=3, choices=Carrera.choices)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-fecha_registro",)
        verbose_name = "estudiante"
        verbose_name_plural = "estudiantes"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(edad__gte=16, edad__lte=100),
                name="estudiante_edad_entre_16_y_100",
            ),
            models.UniqueConstraint(
                Lower("correo"), name="estudiante_correo_unico_sin_mayusculas"
            ),
        ]

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.cedula})"
