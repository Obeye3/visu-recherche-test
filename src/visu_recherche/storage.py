"""Chargement et validation du format d'échange JSON."""

import json
from importlib.resources import files
from pathlib import Path


def validate_publications(value):
    if not isinstance(value, dict):
        raise ValueError("Le corpus JSON doit être un objet indexé par identifiant de publication.")
    cleaned = {}
    for hal_id, row in value.items():
        if not isinstance(hal_id, str) or not hal_id.strip() or not isinstance(row, dict):
            raise ValueError(
                "Chaque publication doit avoir un identifiant et un objet de métadonnées."
            )
        row = row.copy()
        for field in ("title", "abstract", "pdf_link", "type"):
            if row.get(field) is not None and not isinstance(row[field], str):
                raise ValueError(f"{hal_id} : {field} doit être du texte.")
        for field in ("authors", "keywords"):
            items = row.get(field) or []
            if not isinstance(items, list) or not all(isinstance(item, str) for item in items):
                raise ValueError(f"{hal_id} : {field} doit être une liste de textes.")
            row[field] = items
        year = row.get("year")
        if year is not None:
            if isinstance(year, bool) or not str(year).isdigit() or len(str(year)) != 4:
                raise ValueError(f"{hal_id} : l'année doit comporter quatre chiffres.")
            row["year"] = str(year)
        cleaned[hal_id] = row
    return cleaned


def load_publications(path=None):
    source = Path(path) if path else files("visu_recherche").joinpath("data/demo.json")
    return validate_publications(json.loads(source.read_text(encoding="utf-8-sig")))


def save_publications(publications, path):
    destination = Path(path)
    validated = validate_publications(publications)
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Ne pas écraser un corpus existant à la suite d'une erreur de chemin.
    with destination.open("x", encoding="utf-8") as stream:
        json.dump(validated, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
