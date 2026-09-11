"""Extraction d'abstracts ; un échec ne devient jamais un document du corpus."""

import re

import pymupdf

from .network import fetch_bytes


def abstract_from_text(text):
    text = text.replace("\u00ad", "")
    text = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)
    match = re.search(
        r"(?:\babstract\b|\brésumé\b)\s*[:.\-—–]?\s*(.+?)"
        r"(?=\n\s*(?:(?:\d+(?:\.\d+)*|[IVX]+)\s*[.)]?\s*)?"
        r"(?:introduction|index terms|keywords|mots[- ]clés)\b)",
        text,
        re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return None
    abstract = " ".join(match.group(1).split())
    return abstract if len(abstract.split()) >= 8 else None


def extract_abstract(pdf_url):
    content = fetch_bytes(pdf_url)
    if not content.lstrip().startswith(b"%PDF-"):
        raise ValueError("La réponse reçue n'est pas un PDF.")
    # Ouverture en mémoire : aucun fichier temporaire oublié sur disque.
    with pymupdf.open(stream=content, filetype="pdf") as document:
        text = "\n".join(document[index].get_text() for index in range(min(3, len(document))))
    return abstract_from_text(text)
