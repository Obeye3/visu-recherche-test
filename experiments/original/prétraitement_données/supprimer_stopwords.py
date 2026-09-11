import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from langdetect import detect

# Télécharger les stop words français
nltk.download('stopwords')
nltk.download('punkt')

#test="Bonjour , I am doing project Artishow"

def langageDetection(string_txt):
    lang = detect(string_txt)
    if lang == "en" :
        lang= "english"
    elif lang == "fr":
        lang = "french"
    return lang



#language = langageDetection(test)
#print(f"Langue détectée : {language}") 

def supprimer_stopwords(texte):
    # Tokenizer le texte
    langue = langageDetection(texte)
    mots = word_tokenize(texte)
    # Charger les stop words français

    stop_words = set(stopwords.words(langue))
    # Filtrer les mots qui ne sont pas des stop words
    mots_filtrés = [mot for mot in mots if mot.lower() not in stop_words]
    # Rejoindre les mots filtrés en une seule chaîne de caractères
    texte_filtré = ' '.join(mots_filtrés)
    return texte_filtré