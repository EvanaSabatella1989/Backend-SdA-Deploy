import os
import django
from django.conf import settings

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "api_autoservice.settings"
)

try:
    django.setup()
    print("✅ Django cargó correctamente")
except Exception as e:
    print("❌ ERROR AL CARGAR DJANGO:")
    print(e)
    input("Presioná ENTER para salir...")
