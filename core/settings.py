"""
core/settings.py — env-driven (reads .env when present), Postgres support via DATABASE_URL,
WhiteNoise for static files, and CORS handling.
"""

import os
from pathlib import Path

# Load .env if present (local dev). Requires python-dotenv package.
# On Render (production) you normally set env vars in the dashboard; load_dotenv will
# do nothing if there's no .env file.
try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

BASE_DIR = Path(__file__).resolve().parent.parent

# try to load .env from project root (only if python-dotenv installed)
if load_dotenv:
    load_dotenv(BASE_DIR / ".env")

def env_bool(v, default=False):
    if v is None:
        return default
    return str(v).strip().lower() in ("true", "1", "yes", "y", "on")

def env_str(v, default=""):
    return str(v).strip() if v is not None else default

# SECRET KEY (support DJANGO_SECRET_KEY or SECRET_KEY)
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY") or os.environ.get("SECRET_KEY")

# DEBUG (support DJANGO_DEBUG or DEBUG). Default False for safety.
DEBUG = env_bool(os.environ.get("DJANGO_DEBUG") or os.environ.get("DEBUG"), False)

# ALLOWED_HOSTS (support DJANGO_ALLOWED_HOSTS or ALLOWED_HOSTS)
_raw_allowed = os.environ.get("DJANGO_ALLOWED_HOSTS") or os.environ.get("ALLOWED_HOSTS") or ""
# split by comma, strip whitespace, and filter empty strings
ALLOWED_HOSTS = [h.strip() for h in _raw_allowed.split(",") if h.strip()]

# If no hosts provided and DEBUG is True, allow localhost for convenience
if not ALLOWED_HOSTS and DEBUG:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1","blogs-52vm.onrender.com"]

# Application definition
INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # serve static in prod
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",       # must be before CommonMiddleware
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# CORS configuration
# Accept either CORS_ALLOW_ALL_ORIGINS or CORS_ALLOWED_ORIGINS (comma-separated)
CORS_ALLOW_ALL_ORIGINS = env_bool(os.environ.get("CORS_ALLOW_ALL_ORIGINS") or os.environ.get("CORS_ALLOW_ALL_ORIGINS"), True)

if not CORS_ALLOW_ALL_ORIGINS:
    _raw = os.environ.get("CORS_ALLOWED_ORIGINS") or os.environ.get("CORS_ALLOWED_ORIGINS", "")
    CORS_ALLOWED_ORIGINS = [o.strip() for o in _raw.split(",") if o.strip()]
else:
    # django-cors-headers ignores CORS_ALLOWED_ORIGINS when allow_all is True
    CORS_ALLOWED_ORIGINS = []

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # add template dirs here if needed
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Database: use DATABASE_URL if present (Postgres on Render), otherwise fallback to sqlite
DATABASE_URL = env_str(os.environ.get("DATABASE_URL") or os.environ.get("DATABASE"))

if DATABASE_URL:
    try:
        import dj_database_url
    except Exception as e:
        raise RuntimeError("dj-database-url is required to parse DATABASE_URL. Install it (pip install dj-database-url).") from e

    DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
else:
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static & media (WhiteNoise)
STATIC_URL = "/static/"
STATIC_ROOT = Path(os.environ.get("STATIC_ROOT", BASE_DIR / "staticfiles"))
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = Path(os.environ.get("MEDIA_ROOT", BASE_DIR / "media"))

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# REST framework
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "api.pagination.PostCursorPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
}

# Production security settings (apply when DEBUG is False)
if not DEBUG:
    if not SECRET_KEY:
        raise Exception("DJANGO_SECRET_KEY or SECRET_KEY environment variable is required when DEBUG=False")
    SECURE_SSL_REDIRECT = env_bool(os.environ.get("SECURE_SSL_REDIRECT"), True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(env_str(os.environ.get("SECURE_HSTS_SECONDS") or 2592000))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Logging - basic console output
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
