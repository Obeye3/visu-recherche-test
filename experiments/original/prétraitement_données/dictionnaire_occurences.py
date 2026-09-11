import requests
from bs4 import BeautifulSoup
import nltk
from collections import defaultdict
from nltk.stem import WordNetLemmatizer
import re
import unicodedata
#Je prend un url puis renvoie un dictionnaire d'occurences après un pré traitement
# Je fais une lemmatisation puis tokenisation 
def scrape_and_store(url):
    try:
        # Envoyer une requête GET à l'URL
        response = requests.get(url)
        response.raise_for_status()  # Vérifie que la requête s'est bien passée
        
        # Parse le contenu HTML de la page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraire tout le texte de la page
        page_text = soup.get_text(separator='\n')
        page_name ="page_content.txt" 
        # Sauvegarder les informations dans un fichier texte
        with open(page_name, "w", encoding="utf-8") as file:
            file.write(page_text)
        
        print("Les informations de la page ont été stockées dans 'page_content.txt'.")
    
    except requests.exceptions.RequestException as e:
        print(f"Une erreur s'est produite : {e}")

# Exemple d'utilisation
url = "https://artishow.r2.enst.fr/project/99/"  # Remplace par l'URL souhaitée
scrape_and_store(url)



# Téléchargement des ressources nécessaires pour nltk
nltk.download('punkt')
nltk.download('wordnet')

def fichier_vers_dictionnaire(filepath):
    lemmatizer = WordNetLemmatizer()
    occurrences = defaultdict(int)

    # Lecture du fichier
    with open(filepath, 'r', encoding='utf-8') as file:
        contenu = file.read().lower()  # Convertir en minuscules
    
    # 1. Enlever les accents
    contenu = enlever_accents(contenu)
    
    # 2. Séparer les mots et les chiffres collés (ex: "chat123" devient "chat 123")
    contenu = re.sub(r'([a-zA-Z])(\d+)', r'\1 \2', contenu)
    contenu = re.sub(r'(\d+)([a-zA-Z])', r'\1 \2', contenu)
    
    # 3. Nettoyage du texte (enlever la ponctuation)
    contenu = re.sub(r'[^\w\s]', '', contenu)
    
    # 4. Tokenisation du texte en mots
    mots = nltk.word_tokenize(contenu)
    
    for mot in mots:
        # Lemmatisation pour ramener les mots à leur forme canonique
        mot_base = lemmatizer.lemmatize(mot)
        # Incrémentation dans le dictionnaire
        occurrences[mot_base] += 1
    
    return dict(occurrences)

def enlever_accents(texte):
    """ Supprime les accents d'une chaîne de caractères. """
    return ''.join(
        c for c in unicodedata.normalize('NFD', texte)
        if unicodedata.category(c) != 'Mn'
    )

# Exemple d'utilisation
fichier = "/home/mboudouh/Downloads/page_content.txt" # ici , le chemin vers le fichier
#fichier = "/home/mboudouh/Downloads/page_content.txt"
resultat = fichier_vers_dictionnaire(fichier)
for mot, count in resultat.items():
    print(f"{mot}: {count}")

