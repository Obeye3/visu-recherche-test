import re

def extraire_abstracts_et_hal_complets(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        contenu = f.read()

    # Découpe les articles en gardant leurs séparateurs (utile pour vérification)
    articles = re.split(r"(?:=+ Article #[0-9]+:.*?=+\n)", contenu)
    
    résultats = []
    for article in articles:
        if not article.strip():
            continue

        # Trouver le code HAL (ex: hal-01234567v1)
        hal_match = re.search(r'\bhal-\d+(v\d+)?\b', article)
        hal_id = hal_match.group() if hal_match else "HAL non trouvé"

        # Trouver l'abstract (mot-clé + tout ce qui suit)
        abstract = "Abstract non trouvé"
        match = re.search(r'(?:Abstract|ABSTRACT)[\s:\-]*\n*(.*)', article, flags=re.IGNORECASE | re.DOTALL)
        if match:
            abstract = match.group(1).strip()

        résultats.append({
            "hal": hal_id,
            "abstract": abstract
        })

    return résultats

# --- Sauvegarde dans un fichier texte ---
résultats = extraire_abstracts_et_hal_complets("articles_cleaned_2.txt")

with open("abstracts_et_hal_complets.txt", "w", encoding="utf-8") as f:
    for i, r in enumerate(résultats, 1):
        f.write(f"Article {i}\n")
        f.write(f"HAL ID : {r['hal']}\n")
        f.write("ABSTRACT :\n")
        f.write(r['abstract'].strip() + "\n")
        f.write("="*80 + "\n")
