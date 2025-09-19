import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def env_bool(v, default=False):
    if v is None: return default
    return str(v).lower() in ("true","1","yes")

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
DEBUG = env_bool(os.environ.get("DJANGO_DEBUG"), False)
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")  # required in prod

# Static files (WhiteNoise)
STATIC_URL = "/static/"
STATIC_ROOT = Path(os.environ.get("STATIC_ROOT", BASE_DIR / "staticfiles"))
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media (use S3 for production; otherwise local MEDIA_ROOT will be ephemeral)
MEDIA_URL = "/media/"
MEDIA_ROOT = Path(os.environ.get("MEDIA_ROOT", BASE_DIR / "media"))

# Database (Postgres via DATABASE_URL)
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    import dj_database_url
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
else:
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3","NAME": BASE_DIR / "db.sqlite3"}}

# Security (when DEBUG=False)
if not DEBUG:
    if not SECRET_KEY:
        raise Exception("DJANGO_SECRET_KEY is required when DEBUG=False")
    SECURE_SSL_REDIRECT = env_bool(os.environ.get("SECURE_SSL_REDIRECT"), True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", 2592000))  # 30 days
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
