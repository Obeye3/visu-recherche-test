"""Lecture des métadonnées BibTeX publiées dans la page S2A."""

import codecs
import logging
import re
from urllib.parse import urljoin, urlparse

import latexcodec  # noqa: F401 -- enregistre le codec latex
from bs4 import BeautifulSoup

from .network import fetch_bytes
from .storage import validate_publications

LOGGER = logging.getLogger(__name__)
PUBLICATIONS_URL = "https://s2a.telecom-paris.fr/publications/"


def _plain(value):
    value = codecs.decode(value, "ulatex")
    return " ".join(value.replace("{", "").replace("}", "").split())


def parse_bibtex_fields(source):
    """Lire le sous-ensemble S2A en temps linéaire, avec accolades imbriquées.

    Les macros et concaténations BibTeX générales ne sont pas interprétées.
    Les champs inutiles restent du texte, ce qui évite de développer des expressions.
    """
    header = re.match(r"\s*@\w+\s*[{(]\s*[^,]+,", source)
    if not header or len(source) > 100_000:
        raise ValueError("Notice absente, invalide ou trop longue.")
    position, fields = header.end(), {}
    while position < len(source):
        while position < len(source) and (source[position].isspace() or source[position] == ","):
            position += 1
        if position >= len(source) or source[position] in "})":
            break
        field = re.match(r"([A-Za-z_][A-Za-z0-9_-]*)\s*=\s*", source[position:])
        if not field:
            raise ValueError("Champ BibTeX invalide.")
        key = field.group(1).lower()
        position += field.end()
        if position >= len(source):
            raise ValueError("Valeur BibTeX manquante.")
        if source[position] in '{"':
            opener = source[position]
            position += 1
            start, depth = position, 1
            while position < len(source):
                char = source[position]
                if char == "\\":
                    position += 2
                    continue
                if opener == "{" and char == "{":
                    depth += 1
                elif (opener == "{" and char == "}") or (opener == '"' and char == '"'):
                    depth -= 1
                    if depth == 0:
                        break
                position += 1
            if depth:
                raise ValueError("Valeur BibTeX non terminée.")
            fields[key] = source[start:position]
            position += 1
        else:
            start = position
            while position < len(source) and source[position] not in ",})":
                position += 1
            fields[key] = source[start:position].strip()
    return fields


def _authors(value):
    names = []
    for part in re.split(r"\s+and\s+", value):
        # BibTeX : nom, prénom ; ou nom, suffixe, prénom.
        parts = [p.strip() for p in part.split(",")]
        if len(parts) == 2:
            part = f"{parts[1]} {parts[0]}"
        elif len(parts) == 3:
            part = f"{parts[2]} {parts[0]} {parts[1]}"
        if name := _plain(part):
            names.append(name)
    return names


def _pdf_url(value, base_url):
    absolute = urljoin(base_url, value)
    parsed = urlparse(absolute)
    if parsed.scheme in {"http", "https"} and parsed.path.lower().endswith(".pdf"):
        return absolute
    return None


def parse_publications(html, base_url=PUBLICATIONS_URL):
    soup = BeautifulSoup(html, "html.parser")
    publications = {}
    for bibliography in soup.select("ol.bibliography"):
        heading = bibliography.find_previous("h3")
        kind = heading.get_text(" ", strip=True) if heading else ""
        for item in bibliography.find_all("li", recursive=False):
            bibtex = item.find("pre")
            if not bibtex:
                continue
            try:
                entry = parse_bibtex_fields(bibtex.get_text())
            except (ValueError, IndexError) as exc:
                LOGGER.warning("Notice BibTeX ignorée : %s", exc)
                continue
            hal_id = _plain(entry.get("hal_id", ""))
            title = _plain(entry.get("title", ""))
            if not hal_id or not title:
                continue
            # Chercher uniquement dans CETTE notice : jamais dans la suivante.
            pdf_link = _pdf_url(entry.get("pdf", ""), base_url)
            if not pdf_link:
                for link in item.find_all("a", href=True):
                    pdf_link = _pdf_url(link["href"], base_url)
                    if pdf_link:
                        break
            abstract = item.select_one(".dropDownAbstract p")
            year = _plain(entry.get("year", ""))
            row = {
                "title": title,
                "authors": _authors(entry.get("author", "")),
                "keywords": [_plain(k) for k in entry.get("keywords", "").split(";") if k.strip()],
                "year": year if re.fullmatch(r"\d{4}", year) else None,
                "type": kind,
                "pdf_link": pdf_link,
                "abstract": abstract.get_text(" ", strip=True) if abstract else "",
            }
            if hal_id not in publications:
                publications[hal_id] = row
            else:
                # Une même publication peut figurer dans plusieurs périodes.
                for field, value in row.items():
                    if not publications[hal_id].get(field) and value:
                        publications[hal_id][field] = value
    return validate_publications(publications)


def collect_publications():
    html = fetch_bytes(PUBLICATIONS_URL, max_bytes=15_000_000)
    result = parse_publications(html)
    if not result:
        raise ValueError("Aucune notice S2A reconnue. La structure du site a peut-être changé.")
    return result
