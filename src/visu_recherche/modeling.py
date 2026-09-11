"""LDA Gensim et export interactif pyLDAvis, sans téléchargement à l'import."""

import re
from functools import lru_cache
from pathlib import Path

FRENCH_STOPWORDS = set(
    """
alors au aux avec ce ces cet cette ceux dans de des du elle elles en entre est et eux
il ils je la le les leur leurs lui mais même ne ni nos notre nous on ou par pas pour
qu que quel quelle qui sa sans se ses son sont sous sur ta te tes toi ton tu un une
vos votre vous c d j l m n s t y a ont être avoir plus ainsi aussi donc dont comme
afin été présente proposons nous avons étude résultats méthode approche articles
""".split()
)


def clean_text(text):
    text = text.replace("\u00ad", "")
    return re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)


@lru_cache(maxsize=2)
def _language_model(language):
    import spacy

    name = "fr_core_news_sm" if language == "fr" else "en_core_web_sm"
    try:
        return spacy.load(name, disable=["parser", "ner"])
    except OSError as exc:
        raise ValueError(
            f"Modèle {name} absent. Voir docs/usage.md pour le mode linguistique."
        ) from exc


def preprocess(documents, *, linguistic=False):
    from gensim.models.phrases import Phraser, Phrases
    from gensim.parsing.preprocessing import STOPWORDS
    from gensim.utils import simple_preprocess

    stopwords = STOPWORDS | FRENCH_STOPWORDS
    tokens = [
        [
            token
            for token in simple_preprocess(clean_text(doc), deacc=True)
            if token not in stopwords
        ]
        for doc in documents
    ]
    threshold = max(5, min(100, len(documents) // 10))
    bigram = Phraser(Phrases(tokens, min_count=5, threshold=threshold))
    trigram = Phraser(Phrases(bigram[tokens], min_count=5, threshold=threshold))
    tokens = [list(trigram[bigram[doc]]) for doc in tokens]
    if not linguistic:
        return tokens

    try:
        from langdetect import DetectorFactory, LangDetectException, detect
    except ImportError as exc:
        raise ValueError("Installer l'option nlp pour activer la lemmatisation.") from exc
    DetectorFactory.seed = 42
    result = []
    for raw, words in zip(documents, tokens, strict=True):
        try:
            language = detect(raw)
        except LangDetectException:
            language = "en"
        try:
            model = _language_model(language)
        except ImportError as exc:
            raise ValueError("Installer l'option nlp pour activer la lemmatisation.") from exc
        result.append(
            [
                token.lemma_.casefold()
                for token in model(" ".join(words))
                if token.pos_ in {"NOUN", "ADJ", "VERB", "ADV"}
                and not token.is_stop
                and len(token.lemma_) > 2
            ]
        )
    return result


def train_lda(corpus, publications, *, num_topics=3, linguistic=False):
    from gensim.corpora import Dictionary
    from gensim.models import LdaModel

    if len(corpus.documents) != len(corpus.ids) or len(set(corpus.ids)) != len(corpus.ids):
        raise ValueError("Les textes et leurs identifiants ne sont pas alignés.")
    if len(corpus.documents) < 2:
        raise ValueError("Il faut au moins deux publications avec un résumé exploitable.")
    if not 2 <= num_topics <= min(30, len(corpus.documents)):
        raise ValueError("Choisir entre 2 et 30 sujets, sans dépasser le nombre de résumés.")
    tokens = preprocess(corpus.documents, linguistic=linguistic)
    dictionary = Dictionary(tokens)
    # Les seuils du prototype supprimaient tout le vocabulaire des petits corpus.
    if len(tokens) >= 10:
        dictionary.filter_extremes(no_below=2, no_above=0.9, keep_n=10_000)
    if not dictionary:
        raise ValueError("Aucun vocabulaire exploitable. Élargir la sélection de publications.")
    bows = [dictionary.doc2bow(words) for words in tokens]
    kept = [index for index, bow in enumerate(bows) if bow]
    omitted = {
        corpus.ids[i]: "Texte vide après prétraitement." for i, bow in enumerate(bows) if not bow
    }
    if len(kept) < num_topics or len(dictionary) < 2:
        raise ValueError(
            "Trop peu de textes ou de mots après prétraitement ; élargir la sélection."
        )
    bows = [bows[i] for i in kept]
    ids = [corpus.ids[i] for i in kept]
    lda = LdaModel(
        corpus=bows,
        id2word=dictionary,
        num_topics=num_topics,
        random_state=42,
        passes=10,
        alpha="auto",
        per_word_topics=False,
    )
    distributions = [lda.get_document_topics(bow, minimum_probability=0) for bow in bows]
    return {
        "lda": lda,
        "corpus": bows,
        "dictionary": dictionary,
        "ids": ids,
        "skipped": corpus.skipped | omitted,
        "topics": [
            {"number": i + 1, "words": [word for word, _ in lda.show_topic(i, topn=10)]}
            for i in range(num_topics)
        ],
        "publications": [
            {
                "id": hal_id,
                "title": publications[hal_id].get("title") or hal_id,
                "authors": publications[hal_id].get("authors") or [],
                "year": publications[hal_id].get("year"),
                "topic": max(probs, key=lambda item: item[1])[0] + 1,
            }
            for hal_id, probs in zip(ids, distributions, strict=True)
        ],
        "preprocessing": "linguistic" if linguistic else "basic",
    }


def visualization_html(result):
    import pyLDAvis
    import pyLDAvis.gensim_models
    from pyLDAvis import urls

    prepared = pyLDAvis.gensim_models.prepare(
        result["lda"],
        result["corpus"],
        result["dictionary"],
        sort_topics=False,
        n_jobs=1,
    )
    # Embarquer les ressources fournies par pyLDAvis : export lisible hors connexion.
    html = pyLDAvis.prepared_data_to_html(
        prepared,
        template_type="simple",
        visid="lda-vis",
        d3_url="__D3__",
        ldavis_url="__LDAVIS__",
        ldavis_css_url="__CSS__",
    )
    css = Path(urls.LDAVIS_CSS_LOCAL).read_text(encoding="utf-8")
    d3 = Path(urls.D3_LOCAL).read_text(encoding="utf-8")
    ldavis = Path(urls.LDAVIS_LOCAL).read_text(encoding="utf-8")
    html = re.sub(r'<link[^>]*href="__CSS__"[^>]*>', lambda _: f"<style>{css}</style>", html)
    for marker, script in (("__D3__", d3), ("__LDAVIS__", ldavis)):
        html = re.sub(
            rf'<script[^>]*src="{marker}"[^>]*>\s*</script>',
            lambda _, source=script: (
                "<script>" + source.replace("</script", "<\\/script") + "</script>"
            ),
            html,
        )
    return (
        '<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Visualisation LDA</title></head><body>'
        + html
        + "</body></html>"
    )


def export_visualization(result, path):
    destination = Path(path)
    html = visualization_html(result)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("x", encoding="utf-8") as stream:
        stream.write(html)
    return destination
