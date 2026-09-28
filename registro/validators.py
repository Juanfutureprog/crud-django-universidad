from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


solo_digitos = RegexValidator(
    regex=r"^\d{10}$",
    message="La cédula debe contener exactamente 10 dígitos.",
)


def validar_cedula_ecuatoriana(valor):
    """Valida una cédula ecuatoriana de persona natural."""
    solo_digitos(valor)
    provincia = int(valor[:2])
    tercer_digito = int(valor[2])
    if not 1 <= provincia <= 24 or tercer_digito >= 6:
        raise ValidationError("Ingrese una cédula ecuatoriana válida.")

    total = 0
    for indice, caracter in enumerate(valor[:9]):
        numero = int(caracter)
        if indice % 2 == 0:
            numero *= 2
            if numero > 9:
                numero -= 9
        total += numero

    digito_verificador = (10 - total % 10) % 10
    if digito_verificador != int(valor[-1]):
        raise ValidationError("Ingrese una cédula ecuatoriana válida.")
