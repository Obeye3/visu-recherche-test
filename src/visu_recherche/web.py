"""Interface Flask locale ; chaque analyse possède son propre fichier résultat."""

import os
import re
import secrets
from pathlib import Path
from threading import Lock
from uuid import uuid4

from flask import Flask, abort, render_template, request, send_from_directory, session

from .corpus import prepare_corpus
from .filtering import filtered_data_dic
from .modeling import export_visualization, train_lda
from .storage import load_publications, validate_publications


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=secrets.token_hex(32),
        MAX_CONTENT_LENGTH=64 * 1024,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Strict",
        DATA_FILE=os.environ.get("VISU_RECHERCHE_DATA"),
        WORK_DIR=os.environ.get("VISU_RECHERCHE_HOME", str(Path.cwd() / ".visu-recherche")),
        DOWNLOAD_PDFS=False,
        LINGUISTIC=False,
    )
    if config:
        app.config.update(config)
    publications = (
        validate_publications(app.config["PUBLICATIONS"])
        if "PUBLICATIONS" in app.config
        else load_publications(app.config["DATA_FILE"])
    )
    output_dir = Path(app.config["WORK_DIR"]).resolve() / "visualizations"
    busy = Lock()
    options = {
        field: sorted(
            {str(item) for row in publications.values() for item in (row.get(field) or [])}
        )
        for field in ("authors", "keywords")
    }
    options["years"] = sorted(
        {str(row["year"]) for row in publications.values() if row.get("year")}, reverse=True
    )

    @app.route("/", methods=["GET", "POST"])
    def index():
        selected = {"authors": [], "keywords": [], "years": []}
        selected.update(num_topics=3, permanent_only=False)
        result, error, result_id, status = None, None, None, 200
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_urlsafe(32)
        if request.method == "POST":
            if not secrets.compare_digest(
                session["csrf_token"], request.form.get("csrf_token", "")
            ):
                abort(400, "Formulaire expiré. Recharger la page.")
            selected.update(
                {key: request.form.getlist(key) for key in ("authors", "keywords", "years")}
            )
            selected["permanent_only"] = request.form.get("permanent_only") == "on"
            if not busy.acquire(blocking=False):
                error, status = (
                    "Une analyse est déjà en cours. Réessayer dans quelques instants.",
                    409,
                )
            else:
                try:
                    try:
                        selected["num_topics"] = int(request.form.get("num_topics", "3"))
                    except ValueError as exc:
                        raise ValueError("Le nombre de sujets doit être un entier.") from exc
                    filtered = filtered_data_dic(publications, selected)
                    if len(filtered) > 500:
                        raise ValueError(
                            "Limiter la sélection à 500 publications pour l'interface locale."
                        )
                    corpus = prepare_corpus(filtered, download_pdfs=app.config["DOWNLOAD_PDFS"])
                    result = train_lda(
                        corpus,
                        filtered,
                        num_topics=selected["num_topics"],
                        linguistic=app.config["LINGUISTIC"],
                    )
                    result_id = uuid4().hex
                    export_visualization(result, output_dir / f"{result_id}.html")
                except ValueError as exc:
                    result, error, status = None, str(exc), 400
                except Exception:
                    app.logger.exception("Échec de l'analyse")
                    result, error, status = (
                        None,
                        "L'analyse a échoué. Consulter le terminal pour le détail.",
                        500,
                    )
                finally:
                    busy.release()
        return render_template(
            "index.html",
            **options,
            selected=selected,
            result=result,
            error=error,
            result_id=result_id,
            total=len(publications),
            demo=not app.config["DATA_FILE"] and "PUBLICATIONS" not in app.config,
            downloads=app.config["DOWNLOAD_PDFS"],
        ), status

    @app.get("/visualizations/<result_id>")
    def visualization(result_id):
        if not re.fullmatch(r"[0-9a-f]{32}", result_id):
            abort(404)
        return send_from_directory(output_dir, f"{result_id}.html")

    @app.after_request
    def headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        return response

    return app
