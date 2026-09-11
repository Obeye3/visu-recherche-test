import os
import re
import requests
from bs4 import BeautifulSoup

# Config
BASE_URL = "https://s2a.telecom-paris.fr/publications/"
INPUT_TXT = "articles_de_publications_permanents.txt"
OUTPUT_TXT = "articles_de_publications_permanents_formatted.txt"

# 1) Récupérer la page HTML et construire un mapping filename → liste d’auteurs
resp = requests.get(BASE_URL)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

author_map = {}
section_re = re.compile(r"(Journal|Conference) Articles", re.I)

for h3 in soup.find_all("h3", string=section_re):
    for sib in h3.find_next_siblings():
        if sib.name in ("h2", "h3"):
            break
        # pour chaque lien PDF dans ce bloc
        for a in sib.find_all("a", href=True):
            href = a['href']
            if not href.lower().endswith(".pdf"):
                continue
            # extraire nom de fichier
            fname = os.path.basename(href.split("?")[0])
            # récupérer le bloc de texte parent, le découper ligne par ligne
            lines = a.find_parent().get_text("\n", strip=True).split("\n")
            # la seconde ligne est typiquement celle des auteurs
            if len(lines) >= 2:
                author_map[fname] = lines[1].strip()
            else:
                author_map[fname] = ""

# 2) Lire le fichier brut et le découper par article
with open(INPUT_TXT, "r", encoding="utf-8") as f:
    contenu = f.read()

# Pattern pour séparer numéros, noms de fichiers et textes
split_re = re.compile(
    r"={10}\s*Article\s*#(\d+)\s*:\s*(.*?)\s*={10}",
    re.DOTALL
)
parts = split_re.split(contenu)
# parts = [avant, num1, fname1, texte1, num2, fname2, texte2, …]

# 3) Générer le fichier formaté
with open(OUTPUT_TXT, "w", encoding="utf-8") as out_f:
    for i in range(1, len(parts), 3):
        num     = parts[i]
        fname   = parts[i+1].strip()
        texte   = parts[i+2].strip()
        auteurs = author_map.get(fname, "")
        # Écriture selon la regex attendue :
        #   Thèse <num> : <texte> @members: <liste auteurs>
        out_f.write(f"Thèse {num} : {texte}\n")
        out_f.write(f"@members: {auteurs}\n\n")

print(f"✓ Formaté : '{OUTPUT_TXT}' prêt pour votre regex !")
