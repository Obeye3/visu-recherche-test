import pytest
import requests


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    """Un test ne doit jamais dépendre de S2A, HAL ou d'un téléchargement de modèle."""

    def forbidden(*args, **kwargs):
        raise AssertionError("Accès réseau inattendu pendant un test")

    monkeypatch.setattr(requests.sessions.Session, "request", forbidden)
