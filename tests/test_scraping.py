import pytest

from visu_recherche.scraping import parse_bibtex_fields, parse_publications


def test_malformed_bibtex_is_rejected_and_nested_fields_are_read():
    with pytest.raises(ValueError, match="non terminée"):
        parse_bibtex_fields("@article{x, title={{never closes}")
    fields = parse_bibtex_fields('@article{x, title={Nested {value}}, year=2024, month="June"}')
    assert fields == {"title": "Nested {value}", "year": "2024", "month": "June"}


def notice(identifier, extra="", title="A nested {scientific} title"):
    return (
        r"<li><pre>@article{x, hal_id={"
        + identifier
        + "}, title={{"
        + title
        + r"}}, author={Cl{\'e}men{\c c}on, St{\'e}phan and {d'Alch\'e-Buc}, Florence}, "
        + extra
        + "}</pre></li>"
    )


def test_bibtex_authors_nested_braces_and_missing_year():
    html = (
        '<h3 class="bibliography">Journal Articles</h3><ol class="bibliography">'
        + notice("hal-one", "year={2024}, keywords={deep learning ; audio},")
        + notice("hal-two")
        + "</ol>"
    )
    result = parse_publications(html)
    assert result["hal-one"]["year"] == "2024"
    assert result["hal-two"]["year"] is None
    assert result["hal-one"]["authors"] == ["Stéphan Clémençon", "Florence d'Alché-Buc"]
    assert result["hal-one"]["title"] == "A nested scientific title"
    assert result["hal-one"]["keywords"] == ["deep learning", "audio"]


def test_pdf_never_leaks_from_next_notice():
    first = notice("hal-one")
    second = notice("hal-two").replace("</li>", '<a href="/file.PDF?download=1">PDF</a></li>')
    result = parse_publications('<ol class="bibliography">' + first + second + "</ol>")
    assert result["hal-one"]["pdf_link"] is None
    assert result["hal-two"]["pdf_link"] == "https://s2a.telecom-paris.fr/file.PDF?download=1"


def test_missing_bibtex_and_duplicate_entries():
    html = (
        '<ol class="bibliography"><li>Unstructured notice</li>'
        + notice("hal-one")
        + notice("hal-one", "year={2025},")
        + "</ol>"
    )
    assert parse_publications(html)["hal-one"]["year"] == "2025"
