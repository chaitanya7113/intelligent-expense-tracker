import os

DEBUG = False
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")
CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",")

_db_url = os.environ.get("DATABASE_URL")
if _db_url:
    import re
    _match = re.match(r"postgres(?:ql)?://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)", _db_url)
    if _match:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": _match.group(5),
                "USER": _match.group(1),
                "PASSWORD": _match.group(2),
                "HOST": _match.group(3),
                "PORT": _match.group(4),
            }
        }

STATIC_ROOT = os.environ.get("STATIC_ROOT", "staticfiles")
