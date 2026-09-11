"""Assemblage ordonné et traçable des textes analysables."""

import logging
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

from .pdf import extract_abstract

LOGGER = logging.getLogger(__name__)
ERROR_PREFIXES = ("erreur lors", "no abstract found", "no pdf link found", "error downloading")


@dataclass
class Corpus:
    documents: list[str]
    ids: list[str]
    skipped: dict[str, str]


def usable_abstract(text):
    if not isinstance(text, str):
        return False
    return len(text.split()) >= 8 and not text.strip().casefold().startswith(ERROR_PREFIXES)


def prepare_corpus(publications, *, download_pdfs=False, workers=4, extractor=extract_abstract):
    if not 1 <= workers <= 8:
        raise ValueError("Le nombre de téléchargements parallèles doit être compris entre 1 et 8.")

    def obtain(item):
        hal_id, publication = item
        text = publication.get("abstract")
        if usable_abstract(text):
            return hal_id, text, None
        if not download_pdfs:
            return hal_id, None, "Résumé absent ou inexploitable ; téléchargement désactivé."
        if not publication.get("pdf_link"):
            return hal_id, None, "Aucun lien PDF."
        try:
            text = extractor(publication["pdf_link"])
        except Exception as exc:
            # Isoler chaque document ; conserver la cause sans entraîner le modèle dessus.
            LOGGER.warning("Extraction impossible pour %s : %s", hal_id, exc)
            return hal_id, None, "Échec du téléchargement ou de la lecture PDF."
        if not usable_abstract(text):
            return hal_id, None, "Résumé non détecté dans le PDF."
        return hal_id, text, None

    corpus = Corpus([], [], {})
    with ThreadPoolExecutor(max_workers=workers) as executor:
        for hal_id, text, reason in executor.map(obtain, publications.items()):
            if reason:
                corpus.skipped[hal_id] = reason
            else:
                corpus.ids.append(hal_id)
                corpus.documents.append(text)
    return corpus
