from unittest.mock import patch

import pytest


pytestmark = pytest.mark.django_db


def test_healthz_returns_200_when_db_reachable(client):
    response = client.get("/healthz/")

    assert response.status_code == 200


def test_healthz_returns_503_when_db_unreachable(client):
    with patch("apps.health.views.connection.cursor", side_effect=Exception):
        response = client.get("/healthz/")

    assert response.status_code == 503
