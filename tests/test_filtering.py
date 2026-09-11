import pytest

from visu_recherche.filtering import filter_publications, filtered_data_dic, normalize

DATA = {
    "one": {
        "authors": ["Florence d’Alché-Buc"],
        "keywords": ["Deep Learning"],
        "year": 2024,
        "type": "Journal Articles",
    },
    "two": {"authors": ["Stéphan  Clémençon"], "keywords": ["optimization"], "year": "2025"},
    "three": {"authors": ["Auteur externe"], "keywords": None, "year": "2025"},
}


def test_empty_selection_keeps_all_publications():
    assert filter_publications(DATA) == DATA


@pytest.mark.parametrize("parameters", [{"years": ["2024"]}, {"year": 2024}])
def test_year_form_key_and_legacy_key(parameters):
    assert list(filtered_data_dic(DATA, parameters)) == ["one"]


def test_accents_apostrophes_and_spaces():
    assert list(filter_publications(DATA, authors=["  florence d'alche-buc "])) == ["one"]
    assert list(filter_publications(DATA, authors=["stephan clemencon"])) == ["two"]
    assert normalize("  Gaël   RICHARD ") == "gael richard"


def test_filters_intersect_but_values_are_alternatives():
    assert list(
        filter_publications(
            DATA, authors=["Stephan Clémençon", "Auteur externe"], years=[2024, 2025]
        )
    ) == ["two", "three"]
    assert filter_publications(DATA, authors=["Stephan Clémençon"], years=[2024]) == {}


def test_permanent_only_is_explicit():
    assert list(filter_publications(DATA, permanent_only=True)) == ["one", "two"]


def test_keywords_are_exact_not_substring_and_do_not_mutate_data():
    assert filter_publications(DATA, keywords=["deep"]) == {}
    assert list(filter_publications(DATA, keywords="DEEP LEARNING")) == ["one"]
    assert DATA["one"]["authors"] == ["Florence d’Alché-Buc"]
