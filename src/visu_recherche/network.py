"""Téléchargements bornés avec TLS vérifié, limités aux hôtes scientifiques attendus."""

from urllib.parse import urljoin, urlparse

import requests

ALLOWED_DOMAINS = ("s2a.telecom-paris.fr", "hal.science", "archives-ouvertes.fr", "arxiv.org")


def validate_url(url):
    parsed = urlparse(url)
    hostname = (parsed.hostname or "").lower().rstrip(".")
    if (
        parsed.scheme not in {"https", "http"}
        or parsed.username
        or parsed.password
        or parsed.port not in {None, 80, 443}
        or not any(
            hostname == domain or hostname.endswith("." + domain) for domain in ALLOWED_DOMAINS
        )
    ):
        raise ValueError("URL refusée : utiliser S2A, HAL ou arXiv, sans identifiants dans l'URL.")
    return url


def fetch_bytes(url, *, max_bytes=25_000_000, timeout=30):
    for _ in range(6):
        validate_url(url)
        with requests.get(
            url,
            timeout=(10, timeout),
            stream=True,
            allow_redirects=False,
            headers={"User-Agent": "visu-recherche/0.1 (research tooling)"},
        ) as response:
            if response.status_code in {301, 302, 303, 307, 308}:
                location = response.headers.get("Location")
                if not location:
                    raise ValueError("Redirection sans destination.")
                url = urljoin(url, location)
                continue
            response.raise_for_status()
            chunks, size = [], 0
            for chunk in response.iter_content(chunk_size=64 * 1024):
                size += len(chunk)
                if size > max_bytes:
                    raise ValueError(f"Document trop volumineux (limite : {max_bytes} octets).")
                chunks.append(chunk)
            return b"".join(chunks)
    raise ValueError("Trop de redirections pendant le téléchargement.")
