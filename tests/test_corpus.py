import pytest

from visu_recherche.corpus import prepare_corpus
from visu_recherche.pdf import abstract_from_text, extract_abstract

TEXT = "This scientific abstract contains enough words to describe a useful research experiment."


def test_offline_mode_never_calls_downloader():
    def forbidden(_):
        pytest.fail("Unexpected network access")

    corpus = prepare_corpus(
        {"a": {"abstract": TEXT}, "b": {"pdf_link": "url"}}, extractor=forbidden
    )
    assert corpus.ids == ["a"]
    assert list(corpus.skipped) == ["b"]


def test_errors_do_not_contaminate_corpus_and_ids_stay_aligned():
    def extractor(url):
        if url == "failed":
            raise TimeoutError("Network unavailable")
        if url == "empty":
            return "No abstract found in the PDF."
        return TEXT + " " + url

    corpus = prepare_corpus(
        {key: {"pdf_link": key} for key in ["one", "failed", "two", "empty"]},
        download_pdfs=True,
        extractor=extractor,
    )
    assert corpus.ids == ["one", "two"]
    assert corpus.documents == [TEXT + " one", TEXT + " two"]
    assert set(corpus.skipped) == {"failed", "empty"}


@pytest.mark.parametrize(
    "heading,end",
    [("ABSTRACT", "1. INTRODUCTION"), ("Résumé", "I Introduction"), ("Abstract", "Index Terms")],
)
def test_abstract_boundaries_and_line_breaks(heading, end):
    text = f"Title\n{heading}—This represen-\ntation contains enough words to describe a useful research experiment.\n{end}\nBody text"
    abstract = abstract_from_text(text)
    assert abstract.startswith("This representation")
    assert "Body text" not in abstract


def test_absent_abstract_is_none():
    assert abstract_from_text("A title\n1 Introduction\nOnly body text.") is None


def test_html_download_is_not_a_pdf(monkeypatch):
    monkeypatch.setattr("visu_recherche.pdf.fetch_bytes", lambda _: b"<html>Sign in</html>")
    with pytest.raises(ValueError, match="PDF"):
        extract_abstract("https://hal.science/file.pdf")


def test_pdf_extraction_in_memory(monkeypatch):
    import pymupdf

    with pymupdf.open() as pdf:
        page = pdf.new_page()
        page.insert_text((70, 70), "Abstract\n" + TEXT + "\n1 Introduction\nBody text.")
        content = pdf.tobytes()
    monkeypatch.setattr("visu_recherche.pdf.fetch_bytes", lambda _: content)
    assert extract_abstract("https://hal.science/file.pdf") == TEXT
