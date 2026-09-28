# Gestión académica de estudiantes

CRUD de estudiantes desarrollado con Django. Incluye autenticación, permisos por operación, validación de cédula ecuatoriana, búsqueda, paginación, administración y pruebas automatizadas.

## Instalación local

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

La aplicación queda disponible en `http://127.0.0.1:8000/`. Los usuarios no administradores deben recibir los permisos `view`, `add`, `change` y/o `delete` de estudiante según su función.

## Configuración

Las variables admitidas están documentadas en `.env.example`. En producción son obligatorias una clave secreta propia, `DJANGO_DEBUG=False` y la lista real de hosts. Django lee las variables del entorno del proceso y no carga archivos `.env` automáticamente.

## Calidad

```powershell
python manage.py check
python manage.py test
python manage.py makemigrations --check --dry-run
```

Antes del despliegue también debe ejecutarse `python manage.py check --deploy` con las variables de producción y configurarse un backend real de correo y una base de datos adecuada para el entorno.

## Importación y exportación de estudiantes

En **Nuevo registro** se puede importar un archivo `.xlsx` de hasta 5 MB o exportar el listado actual. La primera fila del archivo debe contener, exactamente y en este orden:

```text
cedula | nombre | apellido | correo | edad | carrera
```

Los valores admitidos para `carrera` son `SOF`, `ADM`, `DER` y `OTR`. Todas las filas pasan por las mismas validaciones que el formulario manual. La importación es integral: si cualquier fila es inválida o contiene una cédula/correo duplicado, se rechaza el archivo completo y no se guarda ninguna fila.
