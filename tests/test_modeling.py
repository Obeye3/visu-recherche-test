import re

import pytest

from visu_recherche.corpus import Corpus, prepare_corpus
from visu_recherche.modeling import export_visualization, train_lda
from visu_recherche.storage import load_publications


def test_real_lda_pipeline_and_self_contained_html(tmp_path):
    publications = load_publications()
    corpus = prepare_corpus(publications)
    first = train_lda(corpus, publications, num_topics=3)
    second = train_lda(corpus, publications, num_topics=3)
    assert first["ids"] == list(publications)
    assert first["topics"] == second["topics"]
    assert len(first["publications"]) == 12
    assert {row["topic"] for row in first["publications"]} <= {1, 2, 3}
    output = tmp_path / "nested" / "lda.html"
    export_visualization(first, output)
    html = output.read_text(encoding="utf-8")
    assert "__D3__" not in html and "__LDAVIS__" not in html and "__CSS__" not in html
    assert not re.search(r"<script[^>]+src=", html)
    assert "ldavis" in html.lower()
    with pytest.raises(FileExistsError):
        export_visualization(first, output)


def test_empty_corpus_is_an_actionable_error():
    with pytest.raises(ValueError, match="au moins deux"):
        train_lda(Corpus([], [], {}), {})


def test_two_document_corpus_works():
    publications = dict(list(load_publications().items())[:2])
    result = train_lda(prepare_corpus(publications), publications, num_topics=2)
    assert len(result["ids"]) == 2


def test_invalid_topic_count():
    publications = load_publications()
    with pytest.raises(ValueError, match="sans dépasser"):
        train_lda(prepare_corpus(publications), publications, num_topics=13)


def test_empty_vocabulary_is_rejected():
    with pytest.raises(ValueError, match="vocabulaire"):
        train_lda(Corpus(["the and", "the and"], ["a", "b"], {}), {"a": {}, "b": {}}, num_topics=2)
