import re
from Etiquetage_LDA import Dictionnaire_halids_keywords
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
#temp = (documents[0].split('References\n')[1])
#temp2 = re.split(r'\[\d+\]', temp)[23]
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
def pas_de_and(names):
    nom=names
    word= ""
    if(len(nom)>2):
        new_name = nom[-1][4:]
        nom[-1]=new_name
    return nom
def pas_de_and2(names):
    nom= []
    res=[]
    for elt in names:
        nom+=(elt.split("and "))
    for elt in nom:
    
        
        if elt =="":
            continue
        if elt[-1]==" ":
            res.append(elt[:-1])
            continue
        if elt[0]==" ":
            res.append(elt[1:])
            continue
        res.append(elt)
    return res


def clean_noms(temp2):
    noms=[]
    j=0
    for i  in range(len(temp2)):
        word = ""
        try :
            while (temp2[j]!=','):
                if(j>70):
                    return []
                if(temp2[j]=='.'):
                    if(word!=" et al"):
                        noms.append(word[1:])
                    break
                word+=temp2[j]
                j+=1
            if(temp2[j]=='.'):
                break
            noms.append(word[1:])
            #print(j)
            j+=1
        except :
            return pas_de_and2(noms)

    noms=pas_de_and2(noms)
    return noms


def clean_noms_2(temp2):
    noms=[]
    j=0

    for i  in range(len(temp2)):
        word = ""
        try :
            while (temp2[j]!=','):
                if(j>50):
                    return []
                if(temp2[j]=='.' and j>2 and temp2[j-2]==" " and temp2[j-1]!= " "):
                    print(temp2[j+1])
                   #print(temp2[j-2]+temp2[j-1]+temp2[j])
                    ...
                
                elif (temp2[j]=='.'  and j>2):
                    if(word!=" et al"):
                        noms.append(word[1:])
                    break
                word+=temp2[j]
                j+=1
            if(temp2[j]=='.'):
                break
            noms.append(word[1:])
            #print(j)
            j+=1
        except :
            return pas_de_and2(noms)

    noms=pas_de_and2(noms)
    return noms


def recup_citation(doc):
    nom=[]
    dico = Dictionnaire_halids_keywords.load_keywords()
    
    resultat=[]
    for articles in doc :

        reference =articles.split('References\n')
        if(len(reference)==1):
            reference =articles.split('REFERENCES\n')
        if (len(reference)==1):
            continue
      
        fichier = open("data.txt", "a")
        fichier.write('REFERENCES \n')
        fichier.write(reference[-1])
        fichier.write('\n')

        try:
            result = re.findall(r'"(.*?)"', reference[-1])
        except:
            continue
        if(len(temp2)==1):
            continue
        for i in range (1,len(temp2)) :
            temp3 =temp2[i]
            if(len(clean_noms_2(temp3))>=1):
                nom.append(clean_noms_2(temp3))
        if (len(nom)>=1) : 
            resultat.append(nom)
            #dico[getTitre(articles)]
        nom=[]
    return resultat


def recup_citation_2(doc):
    nom=[]
    resultat=[]
    for articles in doc :
        reference =articles.split('References\n')
        if(len(reference)==1):
            reference =articles.split('REFERENCES\n')
        if (len(reference)==1):
            continue
        try:
            temp = re.split(r'\[\d+\]', reference[-1])
        except:
            continue
      
        fichier = open("data.txt", "a")
print(recup_citation(documents))