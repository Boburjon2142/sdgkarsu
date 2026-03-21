import os
from pathlib import Path
from urllib.parse import urlparse

from django.core.exceptions import ImproperlyConfigured


BASE_DIR = Path(__file__).resolve().parent.parent


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_dotenv(BASE_DIR / ".env")


def env(key: str, default=None):
    return os.getenv(key, default)


def env_bool(key: str, default: bool = False) -> bool:
    value = env(key)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_int(key: str, default: int = 0) -> int:
    value = env(key)
    if value is None or value == "":
        return default
    return int(value)


def env_list(key: str, default: str = "") -> list[str]:
    value = env(key, default)
    return [item.strip() for item in value.split(",") if item.strip()]


DEBUG = env_bool("DJANGO_DEBUG", False)
SECRET_KEY = env("DJANGO_SECRET_KEY", "")
if not SECRET_KEY:
    raise ImproperlyConfigured("DJANGO_SECRET_KEY is required.")
if not DEBUG and len(SECRET_KEY) < 50:
    raise ImproperlyConfigured("Use a long random DJANGO_SECRET_KEY in production.")

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS")
if not DEBUG and not ALLOWED_HOSTS:
    raise ImproperlyConfigured("DJANGO_ALLOWED_HOSTS must be set in production.")

CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")
CORS_ALLOWED_ORIGINS = env_list("DJANGO_CORS_ALLOWED_ORIGINS")

if not DEBUG:
    if not CSRF_TRUSTED_ORIGINS:
        raise ImproperlyConfigured("DJANGO_CSRF_TRUSTED_ORIGINS must be set in production.")
    if not CORS_ALLOWED_ORIGINS:
        raise ImproperlyConfigured("DJANGO_CORS_ALLOWED_ORIGINS must be set in production.")
    invalid_csrf_origins = [origin for origin in CSRF_TRUSTED_ORIGINS if not origin.startswith("https://")]
    invalid_cors_origins = [origin for origin in CORS_ALLOWED_ORIGINS if not origin.startswith("https://")]
    if invalid_csrf_origins or invalid_cors_origins:
        raise ImproperlyConfigured("Production CORS and CSRF origins must use HTTPS.")


def database_config_from_url(database_url: str) -> dict:
    parsed = urlparse(database_url)
    scheme = parsed.scheme.lower()
    if scheme in {"sqlite", "sqlite3"}:
        db_path = parsed.path.lstrip("/") or "db.sqlite3"
        return {"ENGINE": "django.db.backends.sqlite3", "NAME": str((BASE_DIR / db_path).resolve())}
    if scheme not in {"postgres", "postgresql", "pgsql"}:
        raise ImproperlyConfigured("Supported DATABASE_URL schemes: sqlite, postgres, postgresql, pgsql.")
    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": parsed.path.lstrip("/"),
        "USER": parsed.username or "",
        "PASSWORD": parsed.password or "",
        "HOST": parsed.hostname or "",
        "PORT": str(parsed.port or "5432"),
        "CONN_MAX_AGE": 60,
        "CONN_HEALTH_CHECKS": True,
    }


DATABASE_URL = env("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///db.sqlite3" if DEBUG else None
if not DATABASE_URL:
    raise ImproperlyConfigured("DATABASE_URL must be set in production. Use PostgreSQL.")

DATABASES = {"default": database_config_from_url(DATABASE_URL)}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "apps.common",
    "apps.accounts",
    "apps.projects",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.common.middleware.RequestContextAuditMiddleware",
    "apps.common.middleware.ContentSecurityPolicyMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 12}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework.authentication.SessionAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_PAGINATION_CLASS": "apps.common.pagination.DefaultPageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
        "apps.common.throttling.LoginRateThrottle",
        "apps.common.throttling.RegisterRateThrottle",
        "apps.common.throttling.SensitiveActionRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "60/min",
        "user": "240/min",
        "login": "5/min",
        "register": "5/hour",
        "sensitive": "10/min",
    },
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FormParser",
    ],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "EXCEPTION_HANDLER": "apps.common.exceptions.api_exception_handler",
}

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = CORS_ALLOWED_ORIGINS
CORS_ALLOW_ALL_ORIGINS = False
CORS_URLS_REGEX = r"^/api/.*$"
CORS_PREFLIGHT_MAX_AGE = 86400
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-language",
    "content-type",
    "x-csrftoken",
    "x-requested-with",
]

SESSION_COOKIE_NAME = "secure_mvp_sessionid"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SAMESITE = "Lax" if DEBUG else "None"
SESSION_COOKIE_AGE = 60 * 60 * 8
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_DOMAIN = env("SESSION_COOKIE_DOMAIN") or None
CSRF_COOKIE_NAME = "secure_mvp_csrftoken"
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SAMESITE = "Lax" if DEBUG else "None"
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_DOMAIN = env("CSRF_COOKIE_DOMAIN") or None

SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", not DEBUG)
SECURE_HSTS_SECONDS = env_int("DJANGO_SECURE_HSTS_SECONDS", 31536000 if not DEBUG else 0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", not DEBUG)
SECURE_HSTS_PRELOAD = env_bool("DJANGO_SECURE_HSTS_PRELOAD", not DEBUG)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
SECURE_CROSS_ORIGIN_RESOURCE_POLICY = "same-site"
X_FRAME_OPTIONS = "DENY"

DATA_UPLOAD_MAX_MEMORY_SIZE = 2 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024
FILE_UPLOAD_PERMISSIONS = 0o640
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o750

CSRF_FAILURE_VIEW = "apps.common.views.csrf_failure"
ADMIN_URL = env("DJANGO_ADMIN_URL", "admin/")

LOG_LEVEL = env("LOG_LEVEL", "INFO")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"structured": {"format": "%(asctime)s %(levelname)s %(name)s %(message)s"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "structured"}},
    "loggers": {
        "django.security": {"handlers": ["console"], "level": "WARNING", "propagate": False},
        "apps.audit": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
        "apps.auth": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
        "": {"handlers": ["console"], "level": LOG_LEVEL},
    },
}

CSP_POLICY = {
    "default-src": ["'self'"],
    "script-src": ["'self'"],
    "style-src": ["'self'", "'unsafe-inline'"],
    "img-src": ["'self'", "data:", "https:"],
    "connect-src": ["'self'"] + CORS_ALLOWED_ORIGINS,
    "font-src": ["'self'", "data:"],
    "object-src": ["'none'"],
    "media-src": ["'self'"],
    "frame-ancestors": ["'none'"],
    "base-uri": ["'self'"],
    "form-action": ["'self'"],
}
