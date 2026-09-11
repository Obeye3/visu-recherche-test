
import os
import re
import requests
from bs4 import BeautifulSoup

from io import BytesIO

# 1. Configuration
BASE_URL = "https://s2a.telecom-paris.fr/publications/"
TARGET_AUTHORS = {
    "Roland Badeau", "Pascal Bianchi", "Philippe Ciblat",
    "Stephan Clémençon", "Florence d'Alché-Buc", "Slim Essid",
    "Olivier Fercoq", "Pavlo Mozharovskyi", "Geoffroy Peeters",
    "Gaël Richard", "François Roueff"
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
hal_id_list = []
for h3 in soup.find_all("h3", string=pattern_section):
    # Parcourir les frères jusqu'à la prochaine section
    for sib in h3.find_next_siblings():
        if sib.name in ("h2", "h3"):
            break

        for li in sib.find_all("li"):
            text = li.get_text(" ", strip=True)
            hal_id_pattern = re.compile(r'hal_id\s*=\s*\{\s*(?P<hal_id>[^}]+)\s*\}', re.IGNORECASE)

            # Rechercher le hal_id dans le texte
            hal_id = None
            match = hal_id_pattern.search(text)
            if match:
                hal_id = match.group("hal_id")
            hal_id_list.append(hal_id)
            # Extraire le lien PDF
            a = li.find("a", href=True)
            if not a:
                continue
            href = a['href']
            if not href.lower().endswith(".pdf"):
                continue

            # Vérifier la présence d'au moins un auteur cible
            block_text = a.find_parent().get_text(separator=" ", strip=True)
            if any(author in block_text for author in TARGET_AUTHORS):
                full_url = href if href.startswith("http") else requests.compat.urljoin(BASE_URL, href)
                pdf_urls.append((hal_id, full_url))

print(hal_id_list)
print(len(hal_id_list))