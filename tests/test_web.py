import re

import pytest
from werkzeug.datastructures import MultiDict

from visu_recherche.web import create_app


@pytest.fixture
def client(tmp_path):
    return create_app({"TESTING": True, "WORK_DIR": tmp_path}).test_client()


def post(client, fields=()):
    page = client.get("/").get_data(as_text=True)
    token = re.search(r'name="csrf_token" value="([^"]+)"', page).group(1)
    return client.post("/", data=MultiDict([("csrf_token", token), *fields]))


def test_home_is_offline_and_labels_synthetic_data(client):
    page = client.get("/")
    assert page.status_code == 200
    assert "textes synthétiques" in page.get_data(as_text=True)
    assert client.get("/static/style.css").status_code == 200


def test_post_runs_when_app_is_imported_and_honors_years(client):
    response = post(client, [("years", "2025"), ("num_topics", "3")])
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "demo-audio-02" in html
    assert "demo-audio-01" not in html
    link = re.search(r'iframe[^>]*src="([^"]+)"', html).group(1)
    visual = client.get(link)
    assert visual.status_code == 200
    assert b"lda-vis" in visual.data
    other = post(client, [("num_topics", "3")]).get_data(as_text=True)
    assert link != re.search(r'iframe[^>]*src="([^"]+)"', other).group(1)


def test_no_results_retains_selection_and_shows_error(client):
    response = post(client, [("years", "1900")])
    assert response.status_code == 400
    assert "au moins deux" in response.get_data(as_text=True)


def test_invalid_topic_count_is_not_internal_error(client):
    assert post(client, [("num_topics", "abc")]).status_code == 400


def test_csrf_and_unknown_output(client):
    assert client.post("/", data={"num_topics": 3}).status_code == 400
    assert client.get("/visualizations/not-a-result").status_code == 404
    assert client.get("/visualizations/" + "a" * 32).status_code == 404
