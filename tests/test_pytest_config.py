from django.conf import settings


def test_pytest_uses_development_settings():
    assert settings.SETTINGS_MODULE == "config.settings.development"
