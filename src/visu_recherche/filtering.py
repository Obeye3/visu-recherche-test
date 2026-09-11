"""Filtres combinables, indépendants du réseau et du modèle scientifique."""

import unicodedata

# Liste du prototype de juin 2025, volontairement figée pour les comparaisons.
PERMANENT_AUTHORS = (
    "Roland Badeau",
    "Pascal Bianchi",
    "Philippe Ciblat",
    "Stephan Clémençon",
    "Florence d'Alché-Buc",
    "Slim Essid",
    "Olivier Fercoq",
    "Pavlo Mozharovskyi",
    "Geoffroy Peeters",
    "Gaël Richard",
    "François Roueff",
    "Maria Boritchev",
    "Radu Dragomir",
    "Mathieu Fontaine",
    "Ekhiñe Irurozki",
    "Yann Issartel",
    "Hicham Janati",
    "Ons Jelassi",
    "Matthieu Labeau",
    "Charlotte Laclau",
    "Laurence Likforman-Sulem",
    "Yves Grenier",
)


def normalize(value: str) -> str:
    """Ignore casse, accents, variantes d'apostrophes/tirets et espaces multiples."""
    value = unicodedata.normalize("NFKD", value.casefold())
    value = "".join(c for c in value if not unicodedata.combining(c))
    value = value.translate(str.maketrans({"’": "'", "‘": "'", "–": "-", "‑": "-"}))
    return " ".join(value.split())


def _values(value):
    if value is None:
        return []
    return [value] if isinstance(value, (str, int)) else list(value)


def filter_publications(
    publications, *, keywords=None, authors=None, years=None, types=None, permanent_only=False
):
    """OU dans chaque filtre, ET entre filtres ; sélection vide = aucune restriction."""
    desired_keywords = {normalize(k) for k in _values(keywords)}
    desired_authors = {normalize(a) for a in _values(authors)}
    desired_years = {str(y) for y in _values(years)}
    desired_types = {normalize(t) for t in _values(types)}
    permanent = {normalize(a) for a in PERMANENT_AUTHORS}
    result = {}
    for hal_id, publication in publications.items():
        names = {normalize(a) for a in publication.get("authors") or []}
        words = {normalize(k) for k in publication.get("keywords") or []}
        if desired_authors and not desired_authors.intersection(names):
            continue
        if permanent_only and not permanent.intersection(names):
            continue
        if desired_keywords and not desired_keywords.intersection(words):
            continue
        if desired_years and str(publication.get("year")) not in desired_years:
            continue
        if desired_types and normalize(publication.get("type") or "") not in desired_types:
            continue
        result[hal_id] = publication
    return result


def filtered_data_dic(publications, parameters):
    """Adaptateur pour les dictionnaires de paramètres du prototype historique."""
    return filter_publications(
        publications,
        keywords=parameters.get("keywords"),
        authors=parameters.get("authors"),
        years=parameters.get("years", parameters.get("year")),
        types=parameters.get("types"),
        permanent_only=parameters.get("permanent_only", False),
    )
