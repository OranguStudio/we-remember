import os

os.environ.setdefault("DJANGO_SECRET_KEY", "test-secret-key")
os.environ.setdefault("DJANGO_DEBUG", "True")
os.environ.setdefault("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")
os.environ.setdefault("DJANGO_LANGUAGE_CODE", "en-us")
os.environ.setdefault("DJANGO_TIME_ZONE", "UTC")
