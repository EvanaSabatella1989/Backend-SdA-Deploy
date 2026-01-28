import os
from pathlib import Path
from datetime import timedelta
import cloudinary
import cloudinary.uploader
import cloudinary.api
from decouple import config
import dj_database_url







# configuracion para recibir las reservas y recuperar contraseñas
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = config('EMAIL_HOST')
#EMAIL_PORT = config('EMAIL_PORT', cast=int)
#EMAIL_HOST_USER = config('EMAIL_HOST_USER')
#EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
#EMAIL_USE_TLS = True
#EMAIL_USE_SSL = False
#EMAIL_TIMEOUT = 10
#DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
#ADMIN_EMAIL = EMAIL_HOST_USER


EMAIL_BACKEND = config(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.smtp.EmailBackend'
)

EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)

EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER








# evitar que se cierre sesion
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),  #
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
}

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)
# DEBUG = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

# ALLOWED_HOSTS = ["backend-sda-deploy.onrender.com"]

if config("RENDER", default=False, cast=bool):
    ALLOWED_HOSTS = ["backend-sda-deploy.onrender.com"]
else:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]



# Application definition

INSTALLED_APPS = [
    'user',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',
    'cloudinary_storage',
    'rest_framework_simplejwt',
    'producto',
    'categoria',
    'venta',
    'venta_detalle',
    'sucursal',
    'turno',
    'reserva',
    'servicio',
    'vehiculo',
    'rest_framework',
    "corsheaders",
    'carrito',
    'django_extensions',
    'contacto',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api_autoservice.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'api_autoservice.wsgi.application'

# CORDS
CORS_ORIGIN_WHITELIST = [
    # 'http://localhost:4200',
    # 'http://127.0.0.1:4200',
    # 'https://evanasabatella1989.github.io/Frontend-SdA-Deploy/'
    'https://evanasabatella1989.github.io'
]



CORS_ALLOW_ALL_ORIGINS = True  # desactivar para producción

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:4200',
    'http://127.0.0.1:4200',
    # 'https://evanasabatella1989.github.io/Frontend-SdA-Deploy/',
    "https://evanasabatella1989.github.io",
]


# Base de datos
if config("RENDER", default=False, cast=bool):
    # Usar PostgreSQL en Render
    DATABASES = {
        'default': dj_database_url.config(
            default=config("DATABASE_URL"),
            conn_max_age=600
        )
    }
else:
    # Usar MySQL localmente
    DATABASES = {
        'default': {
            'ENGINE': 'mysql.connector.django',
            'NAME': config("DB_NAME", default="autoservice"),
            'USER': config("DB_USER", default="root"),
            'PASSWORD': config("DB_PASSWORD", default="root"),
            'HOST': config("DB_HOST", default="localhost"),
            'PORT': config("DB_PORT", default="3306"),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# para que la imagen cargue
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_ROOT = os.path.join(os.path.dirname(
    os.path.dirname(__file__)), 'static', 'static-only')

STATICFILES_DIRS = [
    # BASE_DIR / 'photos',
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'),
]

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(os.path.dirname(__file__)),
                 'static', 'templates'),
)

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL ="user.UserAccount"


# REST_FRAMEWORK = {
#   'DEFAULT_AUTHENTICATION_CLASSES': (
#      'rest_framework_simplejwt.authentication.JWTAuthentication',
# )
# }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # ),
}

APPEND_SLASH = True

FRONTEND_URL = "https://evanasabatella1989.github.io/Frontend-SdA-Deploy"

# CORS_ALLOW_ALL_ORIGINS = True  # Habilita CORS para todas las solicitudes
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    # "https://evanasabatella1989.github.io/Frontend-SdA-Deploy/",
    "https://evanasabatella1989.github.io",
    "https://backend-sda-deploy.onrender.com",
]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config("CLOUD_NAME"),
    'API_KEY': config("API_KEY"),
    'API_SECRET': config("API_SECRET")
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'