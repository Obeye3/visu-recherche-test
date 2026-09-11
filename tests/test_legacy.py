import pytest

from visu_recherche.legacy import attach_abstracts, parse_legacy_abstracts

TEXT = "This scientific abstract contains enough words to describe a useful research experiment."


def test_legacy_format_and_versioned_identifiers():
    text = "Article 1\nHAL ID : hal-123v2\nABSTRACT :\n" + TEXT + "\n========\n"
    abstracts = parse_legacy_abstracts(text)
    result, matched, missing = attach_abstracts({"hal-123": {"title": "Title"}}, abstracts)
    assert result["hal-123"]["abstract"] == TEXT
    assert matched == {"hal-123"}
    assert not missing


def test_conflicting_versions_are_not_silently_merged():
    text = f"HAL ID : hal-123\nABSTRACT :\n{TEXT}\n=======\nHAL ID : hal-123v2\nABSTRACT :\n{TEXT} Different version."
    with pytest.raises(ValueError, match="différents"):
        parse_legacy_abstracts(text)
