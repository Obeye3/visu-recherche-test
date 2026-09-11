import pytest

from visu_recherche.network import fetch_bytes, validate_url


@pytest.mark.parametrize(
    "url",
    [
        "file:///etc/passwd",
        "http://127.0.0.1/private",
        "https://hal.science.evil.test/a.pdf",
        "https://user:pass@hal.science/a.pdf",
        "https://hal.science:8080/a.pdf",
    ],
)
def test_rejects_unexpected_destinations(url):
    with pytest.raises(ValueError):
        validate_url(url)


def test_accepts_hal_subdomain():
    assert validate_url("https://telecom-paris.hal.science/a.pdf")


class Response:
    def __init__(self, status=200, headers=None, chunks=()):
        self.status_code, self.headers, self.chunks = status, headers or {}, chunks

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def raise_for_status(self):
        pass

    def iter_content(self, chunk_size):
        return iter(self.chunks)


def test_redirect_is_checked_before_following(monkeypatch):
    calls = []

    def get(url, **kwargs):
        calls.append(url)
        return Response(302, {"Location": "http://localhost/private"})

    monkeypatch.setattr("visu_recherche.network.requests.get", get)
    with pytest.raises(ValueError):
        fetch_bytes("https://hal.science/a.pdf")
    assert len(calls) == 1


def test_download_size_is_bounded(monkeypatch):
    monkeypatch.setattr(
        "visu_recherche.network.requests.get", lambda *a, **kw: Response(chunks=[b"123", b"456"])
    )
    with pytest.raises(ValueError, match="volumineux"):
        fetch_bytes("https://hal.science/a.pdf", max_bytes=5)
