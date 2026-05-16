from django.apps import apps
from django.conf import settings
from django.test import override_settings


def test_django_boots():
    assert apps.ready


def test_settings_load():
    assert settings.SECRET_KEY
    assert settings.ROOT_URLCONF == "config.urls"


@override_settings(ALLOWED_HOSTS=["testserver"])
def test_client_returns_response(client):
    response = client.get("/")

    assert response.status_code in {200, 301, 302, 403, 404}
