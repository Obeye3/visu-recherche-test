"""Créer une archive de la sélection Git, sans corpus ou résultats locaux."""

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from check_repository import ROOT, inspect


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    paths, size, failures = inspect()
    if failures:
        raise SystemExit("Corriger les anomalies avec scripts/check_repository.py avant l'export.")
    # L'archive doit rester extérieure au dépôt pour ne pas s'inclure au prochain export.
    destination = args.output.resolve()
    if destination.is_relative_to(ROOT):
        raise SystemExit("Choisir une destination extérieure au dossier du dépôt.")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(destination, "x", compression=ZIP_DEFLATED) as archive:
        for relative in paths:
            archive.write(ROOT / relative, "visu-recherche/" + relative)
    print(f"{len(paths)} fichiers ({size:,} octets avant compression) : {destination}")


if __name__ == "__main__":
    main()
