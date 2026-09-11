"""Contrôler les fichiers sélectionnés par Git, sans afficher de valeurs secrètes."""

import ast
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL_PREFIXES = ("data/local/", "results/", "docs/reports/local/", ".visu-recherche/")
SECRET_PATTERNS = (
    r"gh[pousr]_[A-Za-z0-9]{30,}",
    r"github_pat_[A-Za-z0-9_]{30,}",
    r"sk-(?:proj-)?[A-Za-z0-9_-]{30,}",
    r"AKIA[A-Z0-9]{16}",
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
)


def candidate_paths():
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        check=True,
        capture_output=True,
    )
    return sorted({path.decode("utf-8") for path in result.stdout.split(b"\0") if path})


def inspect():
    failures, total = [], 0
    paths = candidate_paths()
    for relative in paths:
        path = ROOT / relative
        if not path.is_file():
            failures.append(f"Fichier référencé mais absent : {relative}")
            continue
        total += path.stat().st_size
        if relative.startswith(LOCAL_PREFIXES) or path.name in {".env", ".DS_Store"}:
            failures.append(f"Fichier local sélectionné par Git : {relative}")
        if path.stat().st_size > 10_000_000:
            failures.append(f"Fichier de plus de 10 Mo à examiner : {relative}")
        if path.suffix in {".png", ".jpg", ".pdf", ".zip", ".whl", ".docx", ".pptx"}:
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            failures.append(f"Fichier texte non UTF-8 : {relative}")
            continue
        if path.suffix == ".py":
            try:
                ast.parse(text, filename=relative)
            except SyntaxError as exc:
                failures.append(f"Syntaxe Python : {relative}:{exc.lineno} : {exc.msg}")
        if any(re.search(pattern, text) for pattern in SECRET_PATTERNS):
            failures.append(f"Motif de secret possible : {relative}")
    return paths, total, failures


if __name__ == "__main__":
    try:
        paths, size, failures = inspect()
    except subprocess.CalledProcessError:
        raise SystemExit("Initialiser le dépôt avec git init -b main avant ce contrôle.") from None
    for failure in failures:
        print(failure)
    print(f"{len(paths)} fichiers destinés à Git ; {size:,} octets ; {len(failures)} anomalie(s).")
    print("Contrôle ciblé de motifs de secrets ; il ne remplace pas une revue du contenu.")
    raise SystemExit(bool(failures))
