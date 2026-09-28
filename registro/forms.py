from django import forms

from .models import Estudiante


class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ["cedula", "nombre", "apellido", "correo", "edad", "carrera"]
        widgets = {
            "cedula": forms.TextInput(
                attrs={"placeholder": "Ej. 0926687854", "inputmode": "numeric"}
            ),
            "nombre": forms.TextInput(
                attrs={"placeholder": "Ej. Rodrigo Josué", "autocomplete": "given-name"}
            ),
            "apellido": forms.TextInput(
                attrs={"placeholder": "Ej. Guevara Reyes", "autocomplete": "family-name"}
            ),
            "correo": forms.EmailInput(
                attrs={"placeholder": "estudiante@correo.com", "autocomplete": "email"}
            ),
            "edad": forms.NumberInput(attrs={"min": 16, "max": 100}),
        }

    def clean_correo(self):
        return self.cleaned_data["correo"].strip().lower()

    def clean_nombre(self):
        return " ".join(self.cleaned_data["nombre"].split()).title()

    def clean_apellido(self):
        return " ".join(self.cleaned_data["apellido"].split()).title()


class EstudianteUpdateForm(EstudianteForm):
    class Meta(EstudianteForm.Meta):
        fields = ["correo", "edad", "carrera"]
