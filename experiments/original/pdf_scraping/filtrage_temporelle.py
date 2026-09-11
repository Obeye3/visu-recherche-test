import re

def split_articles(input_path, recent_path, old_path):
    """
    Lit un fichier .txt où chaque article commence par un caractère form-feed (\f, affiché ^L),
    et contient une ligne "Submitted on DD Mon YYYY" ou "last revised DD Mon YYYY".
    Sépare les articles en deux fichiers :
      - recent_path : articles dont l'année (souvent issue de 'Submitted on' ou 'last revised') est ≥ 2023
      - old_path    : articles dont l'année est < 2023 (ou qui n'ont pas de date trouvée)
    """

    # Lecture du contenu brut du fichier
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # On découpe chaque article sur le caractère form-feed (LF 0x0C)
    # Attention : dans le .txt, ce caractère peut apparaître en tant que '\f' ou '^L'
    # Dans Python, on le repère avec '\f' (code ASCII 12).
    articles = content.split('\f')
    # On nettoie d'éventuels éléments vides en début ou fin
    articles = [art.strip() for art in articles if art.strip()]

    recent_articles = []
    old_articles = []

    # Regex pour attraper un éventuel "Submitted on DD Mon YYYY" ou "last revised DD Mon YYYY"
    # On capture l'année (\d{4}) après le jour et le mois (lettres en anglais/français)
    date_regex = re.compile(r'(?:Submitted on|last revised)\s+\d{1,2}\s+\w+\s+(\d{4})', re.IGNORECASE)

    for art in articles:
        # Cherche d'abord "last revised"; si absent, cherche "Submitted on"
        # (on prend la première correspondance trouvée pour en extraire l'année)
        m = date_regex.search(art)
        if m:
            year = int(m.group(1))
            if year >= 2023:
                recent_articles.append(art)
            else:
                old_articles.append(art)
        else:
            # Si aucune date valable n'est trouvée, on considère l'article comme "ancien"
            old_articles.append(art)

    # Écriture des articles récents (>=2023) dans le fichier recent_path
    with open(recent_path, 'w', encoding='utf-8') as fout:
        for a in recent_articles:
            fout.write(a + '\n\n')

    # Écriture des articles anciens (<2023 ou sans date) dans le fichier old_path
    with open(old_path, 'w', encoding='utf-8') as fout:
        for a in old_articles:
            fout.write(a + '\n\n')


    # Exemple d'appel
    # Remplacez 'input.txt' par le chemin vers votre fichier source,
    # et 'recent.txt' / 'old.txt' par les chemins souhaités pour la sortie.
split_articles('../pdf_scraping/articles_de_publications_permanents_formatted.txt', 'recent.txt', 'old.txt')
