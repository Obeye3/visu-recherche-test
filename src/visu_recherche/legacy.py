"""Réutiliser les abstracts saisis dans le corpus historique du projet."""

import re

from .corpus import usable_abstract


def base_hal_id(identifier):
    return re.sub(r"v\d+$", "", identifier.strip(), flags=re.IGNORECASE)


def parse_legacy_abstracts(text):
    abstracts = {}
    pattern = r"HAL\s+ID\s*:\s*(\S+)\s*\nABSTRACT\s*:\s*\n(.*?)(?=\n={5,}|\Z)"
    for match in re.finditer(pattern, text, re.IGNORECASE | re.DOTALL):
        identifier, abstract = match.groups()
        abstract = abstract.strip()
        if not usable_abstract(abstract):
            continue
        key = base_hal_id(identifier)
        if key in abstracts and abstracts[key] != abstract:
            raise ValueError(f"Plusieurs résumés différents pour {key} dans le fichier historique.")
        abstracts[key] = abstract
    if not abstracts:
        raise ValueError("Aucun résumé reconnu. Format attendu : HAL ID : … puis ABSTRACT : …")
    return abstracts


def attach_abstracts(publications, abstracts):
    result = {key: row.copy() for key, row in publications.items()}
    matched = set()
    for identifier, row in result.items():
        key = base_hal_id(identifier)
        if key in abstracts:
            row["abstract"] = abstracts[key]
            row["abstract_source"] = "Corpus historique fourni avec le projet"
            matched.add(key)
    return result, matched, set(abstracts) - matched
