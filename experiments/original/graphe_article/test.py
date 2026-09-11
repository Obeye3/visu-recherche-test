import re
from Dictionnaire_halids_keywords_temp import load_keywords
from graph_to_csv import write_to_file
import requests
import tempfile
import fitz  # PyMuPDF
from requests.exceptions import RequestException
dico = {}

def conversion_txt_string(nom_fichier):
    try:
        with open(nom_fichier, "r", encoding="utf-8") as fichier:
            contenu = fichier.read()
        return contenu
    
    except FileNotFoundError:
        return "Erreur : fichier non trouvé."
    except Exception as e:
        return f"Erreur : {e}"
tempo = conversion_txt_string("../pdf_scraping/articles_de_publications_permanents_formatted.txt")
documents = re.split(r'Thèse \d+ *:', tempo)
documents=documents[1:]

CANONICAL_AUTHORS = {
    "Roland Badeau", "Pascal Bianchi", "Philippe Ciblat",
    "Stephan Clémençon", "Florence d'Alché-Buc", "Slim Essid",
    "Olivier Fercoq", "Pavlo Mozharovskyi", "Geoffroy Peeters",
    "Gaël Richard", "François Roueff", "Maria Boritchev",
    "Radu Dragomir", "Mathieu Fontaine", "Ekhiñe Irurozki",
    "Yann Issartel", "Hicham Janati", "Ons Jelassi",
    "Matthieu Labeau", "Charlotte Laclau",
    "Laurence Likforman-Sulem", "Yves Grenier",
}
def extract_references_from_pdf(pdf_url):
    print("Beginning extraction of references...\n")

    if pdf_url is None:
        return []

    # Téléchargement du PDF
    try:
        response = requests.get(pdf_url, timeout=10)
        response.raise_for_status()
    except RequestException as e:
        #print(f"Erreur lors du téléchargement du PDF : {e}")
        return []

    # Sauvegarde temporaire du PDF
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
        tmp_file.write(response.content)
        tmp_pdf_path = tmp_file.name

    # Lecture du PDF avec fitz
    try:
        doc = fitz.open(tmp_pdf_path)
    except Exception as e:
        print(f"Erreur lors de l'ouverture du PDF avec fitz : {e}")
        return []

    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()

    # Recherche de la section des références
    match = re.search(r'(REFERENCES|References)\s*(.+)', text, re.IGNORECASE | re.DOTALL)
    
    if match:
        full_text = match.group(0).strip()
        return [full_text]  # Retourne une liste contenant un seul article (comme attendu par recup_citation_2)

    print("Pas de section 'References' trouvée.")
    return []


def clean(texte):
    temp = texte.lower()
    res =""
    for i in range (len(temp) ):
        if temp[i]=='\n':
            if(i>0 and temp[i-1]=='-'):
                print(texte)
                res= res[:-1]
            else:
                res+= " "
        elif temp[i]==" " and i==0:
            continue
        else:
            res+= temp[i]
    if (len(res)==0):
       return res
    if(res[-1]==','):
        res= res[:-1]
    return res

def nettoyage(new_text):
    res = []
    print(new_text[0])
    if len(new_text[0])>0 and new_text[0][0]==',':

        
        for i in  range(len(new_text)):
            elem=new_text[i]
            if elem[0] != ',' and len(elem)>8:
                return new_text[i:]

        return res
    return new_text


def cherche_titre(text):
    if(text == ''):
        return []
    
    new_text = re.findall(r'“(.*?)”', text, re.DOTALL)
    if(new_text==[]):
         new_text = text.split('.')
         
         if(len(new_text)>1):
            new_text = new_text[1:]
         new_text = nettoyage(new_text)
            #print(new_text)
    if(len(new_text)>0 and len(new_text[0])<300):
        if(len(new_text[0])==0):
            print(text)
            return []
        resultat = clean(new_text[0])

        return [resultat]

    else:
        return []
   
    return ""

def recup_citation_2(doc,titre):
    nom=[]
    resultat={}
    n =1
    for articles in doc :
       
        liste_citation = []
        reference =articles.split('References\n')
        if(len(reference)==1):
     
            reference =articles.split('REFERENCES\n')
        
        if (len(reference)==1):
            continue
        try:
    
            temp = re.split(r'\[\d+\]', reference[-1])
        except:
            continue
        #print(reference)
        fichier = reference[1].split('\n')
        
        try:
            temp = re.split(r'\[\d+\]', reference[-1])
            #print(temp[:10])
        except:
            continue
        for elt in temp :
   
            
            liste_citation +=cherche_titre(elt)
        
        return liste_citation
        
        resultat[titre] =liste_citation
    return resultat
       
def recup_citation(url):
    doc = extract_references_from_pdf(url)
    #print(url)
    if (doc == []):
        return []
    liste_citation = []
    reference =doc.split('References\n')
    if(len(reference)==1):
        reference =doc.split('REFERENCES\n')
    if (len(reference)==1):
        return []
    try:
        temp = re.split(r'\[\d+\]', reference[-1])
    except:
        return []
    #print(reference)
    fichier = reference[1].split('\n')
    try:
        temp = re.split(r'\[\d+\]', fichier)
    except:
        return []
    for elt in temp :

        liste_citation +=cherche_titre(elt)
   
    
    
    #print(liste_citation)
    return liste_citation
doc_references = extract_references_from_pdf("https://hal.science/hal-04762097v1/file/main.pdf")

resultat = recup_citation_2(doc_references,"article")         
print(resultat)