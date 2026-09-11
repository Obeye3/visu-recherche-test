"""Points d'entrée documentés : serve, collect et analyze."""

import argparse
import logging
from pathlib import Path

from .corpus import prepare_corpus
from .filtering import filter_publications
from .storage import load_publications, save_publications


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Explorer des publications scientifiques avec LDA."
    )
    subcommands = parser.add_subparsers(dest="command", required=True)
    serve = subcommands.add_parser("serve", help="Ouvrir l'application locale (démo par défaut).")
    serve.add_argument("--data", type=Path, help="Corpus JSON ; sinon exemple synthétique fourni.")
    serve.add_argument("--port", type=int, default=5000)
    serve.add_argument("--work-dir", type=Path, default=Path(".visu-recherche"))
    serve.add_argument(
        "--download-pdfs", action="store_true", help="Compléter les résumés via le réseau."
    )
    serve.add_argument(
        "--linguistic", action="store_true", help="Activer la lemmatisation spaCy optionnelle."
    )
    collect = subcommands.add_parser(
        "collect", help="Collecter les métadonnées S2A, sans télécharger les PDF."
    )
    collect.add_argument("--output", type=Path, required=True)
    attach = subcommands.add_parser(
        "attach-abstracts", help="Associer les résumés historiques aux métadonnées JSON."
    )
    attach.add_argument("--data", type=Path, required=True)
    attach.add_argument("--abstracts", type=Path, required=True)
    attach.add_argument("--output", type=Path, required=True)
    analyze = subcommands.add_parser(
        "analyze", help="Exporter une visualisation LDA HTML autonome."
    )
    analyze.add_argument("--data", type=Path)
    analyze.add_argument("--output", type=Path, required=True)
    analyze.add_argument("--topics", type=int, default=3)
    analyze.add_argument("--author", action="append", default=[])
    analyze.add_argument("--keyword", action="append", default=[])
    analyze.add_argument("--year", action="append", default=[])
    analyze.add_argument("--permanent-only", action="store_true")
    analyze.add_argument("--download-pdfs", action="store_true")
    analyze.add_argument("--linguistic", action="store_true")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
    try:
        if args.command == "collect":
            from .scraping import collect_publications

            if args.output.exists():
                raise FileExistsError(
                    "Le fichier de destination existe déjà ; choisir un autre nom."
                )
            publications = collect_publications()
            save_publications(publications, args.output)
            print(f"{len(publications)} publications enregistrées : {args.output}")
        elif args.command == "attach-abstracts":
            from .legacy import attach_abstracts, parse_legacy_abstracts

            abstracts = parse_legacy_abstracts(args.abstracts.read_text(encoding="utf-8-sig"))
            result, matched, unmatched = attach_abstracts(load_publications(args.data), abstracts)
            save_publications(result, args.output)
            print(
                f"{len(matched)} résumés associés ; {len(unmatched)} identifiants sans métadonnées."
            )
            if unmatched:
                print("Non associés : " + ", ".join(sorted(unmatched)))
        elif args.command == "serve":
            from .web import create_app

            if not 1 <= args.port <= 65535:
                raise ValueError("Le port doit être compris entre 1 et 65535.")
            app = create_app(
                {
                    "DATA_FILE": args.data,
                    "WORK_DIR": args.work_dir,
                    "DOWNLOAD_PDFS": args.download_pdfs,
                    "LINGUISTIC": args.linguistic,
                }
            )
            app.run(host="127.0.0.1", port=args.port, debug=False, use_reloader=False)
        else:
            from .modeling import export_visualization, train_lda

            if args.output.exists():
                raise FileExistsError(
                    "Le fichier de destination existe déjà ; choisir un autre nom."
                )
            publications = filter_publications(
                load_publications(args.data),
                authors=args.author,
                keywords=args.keyword,
                years=args.year,
                permanent_only=args.permanent_only,
            )
            corpus = prepare_corpus(publications, download_pdfs=args.download_pdfs)
            result = train_lda(
                corpus, publications, num_topics=args.topics, linguistic=args.linguistic
            )
            export_visualization(result, args.output)
            print(f"{len(result['ids'])} résumés analysés ; {len(result['skipped'])} ignorés.")
            for hal_id, reason in result["skipped"].items():
                print(f"  {hal_id} : {reason}")
            print(f"Visualisation : {args.output.resolve()}")
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Erreur : {exc}\n")
    return 0
