import os
from pathlib import Path
from datetime import timedelta
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

load_dotenv()


def get_bool_env(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")


def get_list_env(name, default=None):
    value = os.getenv(name)
    if value is None:
        return default or []
    return [item.strip() for item in value.split(",") if item.strip()]


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_bool_env("DEBUG", default=True)

ALLOWED_HOSTS = get_list_env("ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])

CORS_ALLOWED_ORIGINS = get_list_env("CORS_ALLOWED_ORIGINS", default=["http://localhost:3000","http://127.0.0.1:3000",],)

CORS_ALLOW_CREDENTIALS = True

# Application definition
BASE_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LOCAL_APPS = [
    "apps.subadmin",
    "apps.base",
    "apps.users",
    "apps.projects",
    "apps.tasks",
    "apps.notifications",
    "apps.comments",
    "apps.documents",
    "apps.company",
]

THIRD_APPS = [
    "rest_framework",
    "corsheaders",
    "simple_history",
    "rest_framework_simplejwt",
    "django_extensions",
    "pgvector.django",
]

INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THIRD_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

ROOT_URLCONF = "wapp.urls"

AUTH_USER_MODEL = "users.User"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

STATIC_ROOT = os.getenv("STATIC_ROOT", os.path.join(BASE_DIR, "staticfiles"))
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATIC_URL = os.getenv("STATIC_URL", "/static/")
MEDIA_URL = "/media/"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

WSGI_APPLICATION = "wapp.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DATABASE_ENGINE"),
        "NAME": os.getenv("DATABASE_NAME"),
        "USER": os.getenv("DATABASE_USER"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD"),
        "HOST": os.getenv("DATABASE_HOST"),
        "PORT": int(os.getenv("DATABASE_PORT", 5432)),
        "CONN_MAX_AGE": 300,
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = os.getenv("LANGUAGE_CODE", "es")

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

UNFOLD = {
    "SITE_TITLE": "Gestión de Proyectos",
    "SITE_HEADER": "Panel Administrativo",
    "SITE_URL": "/admin/",
    "SHOW_COUNTS": True,
    "DASHBOARD": {
        "widgets": [
            {
                "type": "text",
                "title": "Bienvenido",
                "content": "Bienvenido al sistema de gestión de proyectos.",
            },
            {
                "type": "html",
                "title": "Soporte",
                "content": "<a href='mailto:soporte@tusistema.com'>Contactar soporte</a>",
            },
        ]
    },
    "STYLES": [
        lambda request: static("admin/css/admin.css"),
    ],
    "SCRIPTS": [
        lambda request: static("admin/js/jquery-3.6.0.min.js"),
    ],
    "COLORS": {
        "primary": {
            "50": "230 225 235",  # muy claro, casi lavanda gris
            "100": "210 200 225",  # lavanda gris suave
            "200": "180 160 210",  # lavanda media
            "300": "150 120 195",  # tono claro púrpura-gris
            "400": "130 90 180",  # más saturado
            "500": "100 60 160",  # tono base púrpura
            "600": "80 50 140",  # más sobrio
            "700": "65 45 120",  # mezcla gris-púrpura
            "800": "55 40 100",  # oscuro
            "900": "45 35 80",  # muy oscuro
            "950": "35 30 65",  # casi negro con tinte púrpura
        }
    },
}

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
