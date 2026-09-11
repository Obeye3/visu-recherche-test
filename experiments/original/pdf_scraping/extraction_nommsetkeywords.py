#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extraction des entrées BibTeX (journaux + conférences) depuis
https://s2a.telecom-paris.fr/publications/ et sauvegarde dans article.txt
"""

import re
import requests
from pathlib import Path

URL = "https://s2a.telecom-paris.fr/publications/"
OUT_FILE = Path("article.txt")

# 1) Récupération de la page
response = requests.get(URL, timeout=30)
response.raise_for_status()
html = response.text

# 2) Recherche non-gourmande des blocs BibTeX article / inproceedings
bib_pattern = re.compile(
    r"@(?:article|inproceedings)\{[\s\S]+?\n\s*\}",   # non-gourmand jusqu’à la '}' finale
    flags=re.MULTILINE,
)

entries = bib_pattern.findall(html)

# 3) Suppression des doublons tout en conservant l'ordre d'apparition
entries_unique = list(dict.fromkeys(e.strip() for e in entries))

# 4) Écriture dans le fichier
OUT_FILE.write_text("\n\n".join(entries_unique) + "\n", encoding="utf-8")

print(f"{len(entries_unique)} entrées écrites dans {OUT_FILE.resolve()}")
