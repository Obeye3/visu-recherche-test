#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Construire un dictionnaire (clé -> [auteurs, keywords, année, titre])
à partir des entrées BibTeX présentes dans article.txt
"""

import re
import json
import unicodedata
from pathlib import Path

BIB_FILE = Path("article.txt")

# --------------------------------------------------------------------
# 1. Auteur·e·s d'intérêt (forme canonique)
# --------------------------------------------------------------------
CANONICAL_AUTHORS = {
    "Roland Badeau", "Pascal Bianchi", "Philippe Ciblat",
    "Stephan Clémençon", "Florence d'Alché-Buc", "Slim Essid",
    "Olivier Fercoq", "Pavlo Mozharovskyi", "Geoffroy Peeters",
    "Gaël Richard", "François Roueff", "Maria Boritchev",
    "Radu Dragomir", "Mathieu Fontaine", "Ekhiñe Irurozki",
    "Yann Issartel", "Hicham Janati", "Ons Jelassi",
    "Matthieu Labeau", "Charlotte Laclau",
    "Laurence Likforman-Sulem", "Yves Grenier",
}

# --------------------------------------------------------------------
# 2. Petites fonctions utilitaires
# --------------------------------------------------------------------
def strip_accents(text: str) -> str:
    """Enlève les accents, renvoie en minuscules."""
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return text.lower()

# normalisation simple de tous les prénoms et noms canoniques
CANONICAL_TOKENS = {
    full: {strip_accents(t) for t in full.replace("-", " ").split()}
    for full in CANONICAL_AUTHORS
}

# --------------------------------------------------------------------
# 3. Lecture du fichier BibTeX
# --------------------------------------------------------------------
bibtex_text = BIB_FILE.read_text(encoding="utf-8")

# On découpe les entrées sur un « @ » suivi d’un type, jusqu’à la
# accolade fermante correspondante (équilibrage approximatif)
entry_pattern = re.compile(r"@(?:article|inproceedings)\{[\s\S]+?\n\}")
entries = entry_pattern.findall(bibtex_text)

# --------------------------------------------------------------------
# 4. Extraction des informations pour chaque entrée
# --------------------------------------------------------------------
def extract_field(entry: str, field: str) -> str | None:
    """Retourne le contenu du champ BibTeX (sans les accolades), ou None."""
    m = re.search(
        rf"{field}\s*=\s*\{{\s*([\s\S]*?)\s*\}}\s*,?", entry, re.IGNORECASE
    )
    return m.group(1).strip() if m else None


database: dict[str, list] = {}

for entry in entries:
    # clé BibTeX = texte entre '{' et la première virgule
    key_match = re.match(r"@\w+\{([^,]+),", entry)
    if not key_match:
        continue
    bib_key = key_match.group(1).strip()

    # champs utiles
    authors_raw = extract_field(entry, "author") or ""
    title = extract_field(entry, "title") or ""
    keywords_raw = extract_field(entry, "keywords") or ""
    year_raw = extract_field(entry, "year") or ""

    # ----------------------------------------------------------------
    # 4.a Détection des auteur·e·s d'intérêt
    # ----------------------------------------------------------------
    authors_found: list[str] = []
    authors_norm = strip_accents(authors_raw)
    for full_name, tokens in CANONICAL_TOKENS.items():
        if any(token in authors_norm for token in tokens):
            authors_found.append(full_name)

    # ----------------------------------------------------------------
    # 4.b Nettoyage des mots-clés et de l'année
    # ----------------------------------------------------------------
    keywords = (
        [kw.strip() for kw in keywords_raw.split(";") if kw.strip()]
        if keywords_raw
        else []
    )
    try:
        year = int(year_raw)
    except ValueError:
        year = None  # année manquante ou mal formée

    # ----------------------------------------------------------------
    # 4.c Ajout au dictionnaire
    # ----------------------------------------------------------------
    database[bib_key] = [authors_found, keywords, year, title]

# --------------------------------------------------------------------
# 5. Affichage (ou sauvegarde) du résultat
# --------------------------------------------------------------------
print(json.dumps(database, indent=2, ensure_ascii=False))
