import pytest

from visu_recherche.cli import main
from visu_recherche.storage import load_publications, save_publications, validate_publications


@pytest.mark.parametrize(
    "data",
    [
        [],
        {"x": "bad"},
        {"x": {"authors": "Name"}},
        {"x": {"year": True}},
        {"x": {"year": "2024/25"}},
    ],
)
def test_rejects_malformed_corpus(data):
    with pytest.raises(ValueError):
        validate_publications(data)


def test_json_round_trip_and_no_overwrite(tmp_path):
    path = tmp_path / "data" / "corpus.json"
    data = load_publications()
    save_publications(data, path)
    assert load_publications(path) == data
    with pytest.raises(FileExistsError):
        save_publications(data, path)


def test_cli_exports_an_html(tmp_path, capsys):
    path = tmp_path / "output.html"
    assert main(["analyze", "--output", str(path), "--year", "2025"]) == 0
    assert path.exists()
    assert "3 résumés analysés" in capsys.readouterr().out


def test_cli_bad_file_reports_error(tmp_path):
    with pytest.raises(SystemExit) as exc:
        main(
            [
                "analyze",
                "--data",
                str(tmp_path / "missing.json"),
                "--output",
                str(tmp_path / "out.html"),
            ]
        )
    assert exc.value.code == 1
