import os
from pathlib import Path
from urllib.parse import urlparse

from django.core.exceptions import ImproperlyConfigured


BASE_DIR = Path(__file__).resolve().parent.parent


def load_dotenv(dotenv_path):
    if not dotenv_path.exists():
        return

    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


load_dotenv(BASE_DIR / ".env")


def env(key, default=None):
    return os.getenv(key, default)


def env_bool(key, default=False):
    value = env(key)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_int(key, default=0):
    value = env(key)
    if value is None or value == "":
        return default
    return int(value)


def env_list(key, default=""):
    value = env(key, default)
    return [item.strip() for item in value.split(",") if item.strip()]


def database_config_from_url(database_url):
    parsed = urlparse(database_url)
    scheme = parsed.scheme.lower()

    if scheme in {"sqlite", "sqlite3"}:
        db_path = parsed.path.lstrip("/") or "db.sqlite3"
        return {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str((BASE_DIR / db_path).resolve()),
        }

    engine_map = {
        "postgres": "django.db.backends.postgresql",
        "postgresql": "django.db.backends.postgresql",
        "pgsql": "django.db.backends.postgresql",
        "mysql": "django.db.backends.mysql",
    }
    engine = engine_map.get(scheme)
    if not engine:
        raise ImproperlyConfigured(f"Unsupported DATABASE_URL scheme: {scheme}")

    return {
        "ENGINE": engine,
        "NAME": parsed.path.lstrip("/"),
        "USER": parsed.username or "",
        "PASSWORD": parsed.password or "",
        "HOST": parsed.hostname or "",
        "PORT": str(parsed.port or ""),
        "CONN_MAX_AGE": env_int("DJANGO_DB_CONN_MAX_AGE", 60 if not DEBUG else 0),
        "CONN_HEALTH_CHECKS": True,
    }


def cache_config_from_url(cache_url):
    parsed = urlparse(cache_url)
    scheme = parsed.scheme.lower()

    if scheme in {"redis", "rediss"}:
        return {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": cache_url,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
            "KEY_PREFIX": env("DJANGO_CACHE_KEY_PREFIX", "sdg"),
            "TIMEOUT": env_int("DJANGO_CACHE_TIMEOUT", 300),
        }

    if scheme in {"locmem", "memory"}:
        return {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": env("DJANGO_CACHE_LOCATION", "sdg-local-cache"),
            "TIMEOUT": env_int("DJANGO_CACHE_TIMEOUT", 300),
        }

    raise ImproperlyConfigured(f"Unsupported CACHE_URL scheme: {scheme}")


def clone_cache_config(cache_config, *, key_prefix=None):
    cloned = {
        "BACKEND": cache_config["BACKEND"],
        "LOCATION": cache_config["LOCATION"],
        "TIMEOUT": cache_config.get("TIMEOUT"),
    }
    if "OPTIONS" in cache_config:
        cloned["OPTIONS"] = dict(cache_config["OPTIONS"])
    if key_prefix is not None:
        cloned["KEY_PREFIX"] = key_prefix
    elif "KEY_PREFIX" in cache_config:
        cloned["KEY_PREFIX"] = cache_config["KEY_PREFIX"]
    return cloned


SECRET_KEY = env("DJANGO_SECRET_KEY", "change-me-in-production")
DEBUG = env_bool("DJANGO_DEBUG", True)

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost,testserver" if DEBUG else "")
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS", "")

if not DEBUG and SECRET_KEY == "change-me-in-production":
    raise ImproperlyConfigured("Set DJANGO_SECRET_KEY before running with DJANGO_DEBUG=0.")

if not DEBUG and not ALLOWED_HOSTS:
    raise ImproperlyConfigured("Set DJANGO_ALLOWED_HOSTS before running with DJANGO_DEBUG=0.")


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "portal",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "portal.middleware.PortalLanguageMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "config.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]


WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

if env("DATABASE_URL"):
    DATABASES["default"] = database_config_from_url(env("DATABASE_URL"))


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": env("DJANGO_CACHE_LOCATION", "sdg-local-cache"),
        "TIMEOUT": env_int("DJANGO_CACHE_TIMEOUT", 300),
    }
}

if env("CACHE_URL"):
    CACHES["default"] = cache_config_from_url(env("CACHE_URL"))
    CACHES["sessions"] = clone_cache_config(
        CACHES["default"],
        key_prefix=env("DJANGO_SESSION_CACHE_KEY_PREFIX", f'{env("DJANGO_CACHE_KEY_PREFIX", "sdg")}:sessions'),
    )
    CACHES["fragments"] = clone_cache_config(
        CACHES["default"],
        key_prefix=env("DJANGO_FRAGMENT_CACHE_KEY_PREFIX", f'{env("DJANGO_CACHE_KEY_PREFIX", "sdg")}:fragments'),
    )
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "sessions"
else:
    CACHES["sessions"] = clone_cache_config(CACHES["default"], key_prefix="sdg:sessions")
    CACHES["fragments"] = clone_cache_config(CACHES["default"], key_prefix="sdg:fragments")


AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


LANGUAGE_CODE = "en-us"
LANGUAGES = [
    ("uz", "Uzbek"),
    ("en", "English"),
]
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True


STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "assets"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


if not DEBUG:
    SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", True)
    SECURE_HSTS_SECONDS = env_int("DJANGO_SECURE_HSTS_SECONDS", 31536000)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", True)
    SECURE_HSTS_PRELOAD = env_bool("DJANGO_SECURE_HSTS_PRELOAD", True)
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
    X_FRAME_OPTIONS = "DENY"
else:
    SECURE_HSTS_SECONDS = 0
