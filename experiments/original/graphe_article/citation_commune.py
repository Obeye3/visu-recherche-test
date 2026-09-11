import re
from Dictionnaire_halids_keywords_temp import load_keywords
from graph_to_csv import write_to_file
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

def clean(texte):
    temp = texte.lower()
    res =""
    for i in range (len(temp) ):
        if temp[i]=='\n':
            res+= " "
        else:
            res+= temp[i]
    if(res[-1]==','):
        res= res[:-1]
    return res
def cherche_titre(text):
    new_text = re.findall(r'“(.*?)”', text, re.DOTALL)
    if(len(new_text)==1):
         resultat = clean(new_text[0])
         print(resultat)
         return [resultat]

    else:
        return []
   
    return ""

def recup_citation_2(doc):
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
      
        fichier = reference[0].split('\n')
        try:
            temp = re.split(r'\[\d+\]', reference[-1])
        except:
            continue
        for elt in temp :
            liste_citation +=cherche_titre(elt)
        titre = (fichier[0]+" "+fichier[1])

        resultat[titre.lower()] =liste_citation
    return resultat
       
     
def en_commun(dico):
    res ={}
    for articles1 in dico.keys():
        en_comm =[]
        for articles2 in  dico.keys():
            if articles1 != articles2:
                if any(elem in dico[articles1] for elem in dico[articles2]):
                    en_comm.append(articles2)
        res[articles1]=en_comm
    return res


write_to_file(en_commun(recup_citation_2(documents)),"graphe_citation_en_commun1")