import os
import re
import requests
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text
from io import BytesIO

# 1. Configuration
BASE_URL = "https://s2a.telecom-paris.fr/publications/"
TARGET_AUTHORS = {
    "Roland Badeau", "Pascal Bianchi", "Philippe Ciblat",
    "Stephan Clémençon", "Florence d'Alché-Buc", "Slim Essid",
    "Olivier Fercoq", "Pavlo Mozharovskyi", "Geoffroy Peeters",
    "Gaël Richard", "François Roueff", "Maria Boritchev","Radu Dragomir","Mathieu Fontaine","Ekhiñe Irurozki",
    "Yann Issartel", "Hicham Janati", "Ons Jelassi","Matthieu Labeau","Charlotte Laclau","Laurence Likforman-Sulem","Yves Grenier"
}

# 2. Préparer les dossiers
pdf_dir = "pdfs"
os.makedirs(pdf_dir, exist_ok=True)
output_txt = "articles_de_publications_permanents.txt"

# 3. Charger la page et parser
resp = requests.get(BASE_URL)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

# 4. Collecter les URLs des PDF des sections Journal & Conference Articles,
#    en filtrant par auteurs
pdf_urls = []
pattern_section = re.compile(r"(Journal|Conference) Articles", re.I)

for h3 in soup.find_all("h3", string=pattern_section):
    # parcourir les frères jusqu'à la section suivante
    for sib in h3.find_next_siblings():
        if sib.name in ("h2", "h3"):
            break
        # pour chaque lien PDF dans ce segment
        for a in sib.find_all("a", href=True):
            href = a['href']
            if not href.lower().endswith(".pdf"):
                continue
            # extraire le bloc textuel parent pour y rechercher les auteurs
            parent = a.find_parent()
            block_text = parent.get_text(separator=" ", strip=True)
            # vérifier la présence d'au moins un auteur cible
            if any(author in block_text for author in TARGET_AUTHORS):
                full_url = href if href.startswith("http") else requests.compat.urljoin(BASE_URL, href)
                pdf_urls.append(full_url)

# garantir l'unicité
pdf_urls = list(dict.fromkeys(pdf_urls))

# 5. Télécharger, extraire et concaténer le texte
with open(output_txt, "w", encoding="utf-8") as out_f:
    for idx, url in enumerate(pdf_urls, 1):
        try:
            print(f"[{idx}/{len(pdf_urls)}] Traitement : {url}")
            r = requests.get(url)
            r.raise_for_status()

            # sauvegarder localement
            filename = os.path.basename(url.split("?")[0])
            pdf_path = os.path.join(pdf_dir, filename)
            with open(pdf_path, "wb") as f_pdf:
                f_pdf.write(r.content)

            # extraire le texte intégral
            text = extract_text(BytesIO(r.content))

            # écrire dans le fichier de sortie
            out_f.write(f"\n\n========== Article #{idx}: {filename} ==========\n\n")
            out_f.write(text.strip())
            out_f.write("\n\n")

        except Exception as e:
            print(f"Erreur pour {url} : {e}")

print(f"\nTerminé ! Les articles sélectionnés sont dans « {output_txt} ».")
