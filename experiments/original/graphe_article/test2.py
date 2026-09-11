#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Construire un dictionnaire (clé -> [auteurs, keywords, année, titre])
à partir des entrées BibTeX présentes dans article.txt
"""

import re
import json
import unicodedata
from pathlib import Path
from graph_to_csv import write_to_file
from filter_parameters_graph import filtered_data
from load_data_graph import load_data
import networkx as nx
import subprocess
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import requests
import tempfile
import fitz  # PyMuPDF
from requests.exceptions import RequestException
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

dico = load_data()

colorier_voisin = False
afficher_non_cible = False
colorien_lien = True
filtrage_union = False
afficher_noeud_isole= True


dico = filtered_data(dico,None,["2020","2020"],None) # on prend les articles de 2020
#rint(dico)

TARGET_AUTHORS = {
        "Roland  Badeau", "Pascal  Bianchi", "Philippe  Ciblat",
        "Stephan  Clémençon", "Florence  d'Alché-Buc", "Slim  Essid",
        "Olivier  Fercoq", "Pavlo  Mozharovskyi", "Geoffroy  Peeters",
        "Gaël  Richard", "François  Roueff", "Maria  Boritchev",
        "Radu  Dragomir", "Mathieu  Fontaine", "Ekhiñe  Irurozki",
        "Yann  Issartel", "Hicham  Janati", "Ons  Jelassi",
        "Matthieu  Labeau", "Charlotte  Laclau",
        "Laurence  Likforman-Sulem", "Yves  Grenier"
    }

def en_commun(liste1,liste2):
    temp1 = [elem.lower() for elem in liste1]
    temp2 = [elem.lower() for elem in liste2]
    return any(elem in temp1 for elem in temp2) #regarde s'il y a des chaine de caractere en commun

def en_commun(liste1,liste2):
    if(liste1 is None ):
        return False
    if(liste2 is None ):
        return False

    temp1 = [elem.lower() for elem in liste1]
    temp2 = [elem.lower() for elem in liste2]
    
    return any(elem in temp1 for elem in temp2) #regarde s'il y a des chaine de caractere en commun
def id_to_title(id):
    #print(database[id][-1][1:])
    return dico[id]['title']

def id_to_authors(id):
    return dico[id]['authors']

def id_to_keywords(id):
    if (dico[id]['keywords'] is None):
        return []
    return dico[id]['keywords']


def article_permanent(noms):
  
    for permanent in TARGET_AUTHORS:
       
        if permanent in noms or noms in permanent:
            #print(noms + ' = ' + permanent)
            return True
    return False
def generate_graph_authors():
    res = {}
    taille=0
    for id1 in dico.keys():
        res[id1]=[]
        for id2 in dico.keys():
            if id1!=id2:
                liste1 = id_to_authors(id1)
                liste2 = id_to_authors(id2)
                if(en_commun(liste1,liste2)) :
                    taille+=1
                    res[id1].append(id2)
                
            
    return res

def generate_graph_topic():
    res = {}
    for id1 in dico.keys():
        res[id1]=[]
        for id2 in dico.keys():
            if id1!=id2:
                liste1 = id_to_keywords(id1)
                liste2 = id_to_keywords(id2)
                if(en_commun(liste1,liste2)) :
                    res[id1].append(id2)
                
            
    return res

#####################VERSION BERTOPIC ##############

model = SentenceTransformer("all-MiniLM-L6-v2")  # Rapide et léger
sim_matrix= []
def generate_graph_title_similarity(dico, seuil=0.6):
    # 1. Extraire les titres
    ids = list(dico.keys())
    titres = [dico[i]['title'] for i in ids]
    print(ids)

    # 2. Embedding des titres
    embeddings = model.encode(titres, convert_to_numpy=True)

    # 3. Similarité cosinus
    sim_matrix = cosine_similarity(embeddings)
    
    # 4. Création du graphe
    graph = {dico_id: [] for dico_id in ids}

    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            if sim_matrix[i][j] >= seuil:
                graph[ids[i]].append(ids[j])
                graph[ids[j]].append(ids[i])  # symétrique

    return graph

###########################
def authors_article():
    res = {}
    for id in dico.keys():
        for nom in id_to_authors(id):
            res[nom]= []
    for id in dico.keys():
        for nom in id_to_authors(id):
            res[nom] += [id]
    return res


keywords_dic_authors={}
def generate_graph_authors_cowork():
    res = {}
    dictionnaire = authors_article()
    for nom1 in dictionnaire.keys():
        res[nom1]=[]
        temp = []
        for elt in dictionnaire[nom1]:
            temp+= id_to_keywords(elt) 
        keywords_dic_authors[nom1] = temp
        for nom2 in dictionnaire.keys():
            if nom1!=nom2:
                liste1 = dictionnaire[nom1]
                liste2 = dictionnaire[nom2]
                if(en_commun(liste1,liste2)) :
                    res[nom1].append(nom2)
                          
    return res

def generate_graph_authors_sametheme():
    res = {}
    dictionnaire = authors_article()
    for nom1 in dictionnaire.keys():
        res[nom1]=[]
        temp = []
        for elt in dictionnaire[nom1]:
            temp+= id_to_keywords(elt) 
        keywords_dic_authors[nom1] = temp
    for nom1 in dictionnaire.keys():
        for nom2 in dictionnaire.keys():
            if nom1!=nom2:
                liste1 = keywords_dic_authors[nom1]
                liste2 = keywords_dic_authors[nom2]
                if(en_commun(liste1,liste2)) :
                    res[nom1].append(nom2)              
    return res

def transfo(graph):
    res = {}
    for keys in graph.keys():
        res[id_to_title(keys)]=[id_to_title(element) for element in graph[keys]]
    return graph

def author_dic(dictionnary):
    res ={}
    for id in dictionnary.keys():
        sum = ''
        liste_nom = id_to_authors(id)
        for elt in liste_nom:
            sum+=elt + ';'
        sum = sum[:-1]
        res[id] = sum
    return res

def keywords_dic(dictionnary):
    res ={}
    for id in dictionnary.keys():
        sum = ''
        liste_words = id_to_keywords(id)
        for elt in liste_words:
            sum+=elt + ';'
        sum = sum[:-1]
        res[id] = sum
    return res

##################################### GRAPHE DE CITATION #########################################################

def extract_references_from_pdf(pdf_url):
    #print("Beginning extraction of references...\n")

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
        #print(f"Erreur lors de l'ouverture du PDF avec fitz : {e}")
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
                 res= res[:-1]
            else:
                res+= " "
        elif temp[i]==" " and i==0:
            continue
        else:
            res+= temp[i]
    if(len(res)==0):
        return res
    if(res[-1]==','):
        res= res[:-1]
    return res

def nettoyage(new_text):
    res = []
    
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
            #print(new_text)
         nettoyage(new_text)
    if(len(new_text)>0 and len(new_text[0])<300):
         if(len(new_text[0])==0):
            print(text)
            return []
         resultat = clean(new_text[0])

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
        #print(reference)
        fichier = reference[1].split('\n')
        
        try:
            temp = re.split(r'\[\d+\]', reference[-1])
            #print(temp[:10])
        except:
            continue
        for elt in temp :
   
            
            liste_citation +=cherche_titre(elt)
        #print(liste_citation)
        return liste_citation
        
       
    return resultat
      
def process_all_articles_and_save(dico_articles, output_file):
    """
    dico_articles : dict du type { id1: pdf_link1, id2: pdf_link2, ... }
    output_file : chemin du fichier .txt à créer
    """
    print(dico_articles["hal-04044566"]["pdf_link"])
    with open(output_file, "w", encoding="utf-8") as f_out:
        for article_id in dico_articles.keys():
            #print(dico_articles["hal-04044566"]["pdf_link"])
            f_out.write(f"========== ARTICLE --- {article_id} ==========\n")

            doc = extract_references_from_pdf(dico_articles[article_id]["pdf_link"])   # ta fonction adaptée
            liste_citations = recup_citation_2(doc)       # maintenant une liste simple
           
            for citation in liste_citations:
                if(len(citation)>25):
                    f_out.write(citation.strip() + "\n")
           
            f_out.write("\n")  # Séparation entre articles


def lire_citations_depuis_fichier(fichier_txt,dico):
    """
    Parse le fichier texte structuré en blocs d'articles et citations.
    Renvoie un dictionnaire : { article_id: [citation1, citation2, ...] }
    """
    dico_resultat = {}
    article_id = None
    citations = []

    with open(fichier_txt, "r", encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if ligne.startswith("========== ARTICLE ---"):
                # Si on change d'article, on stocke le précédent
                if article_id and citations:
                    if article_id == "hal-04762097":
                        print(citations)
                    if article_id in dico.keys():
                        dico_resultat[article_id] = citations
                # Extraire le nouvel ID
                article_id = ligne.split("ARTICLE ---")[-1].strip("= ").strip()
                citations = []
            elif ligne:  # ignorer lignes vides
                citations.append(ligne)

        # Ajouter le dernier article
        if article_id and citations:
            dico_resultat[article_id] = citations

    return dico_resultat
def citation_en_commun():
    dico_temp = lire_citations_depuis_fichier("citation.txt",dico)
    res ={}
    for articles1 in dico.keys():
        en_comm =[]
        if( articles1 in dico_temp.keys()):
            references1 = [elem for elem in dico_temp[articles1] if len(elem)>25]
            for articles2 in  dico.keys():
                if articles1 != articles2:
                    if( articles2 in dico_temp.keys()):
                        references2 = [elem for elem in dico_temp[articles2] if len(elem)>25]
                        if any(elem in references1 for elem in references2):
                            en_comm.append(articles2)
        res[articles1]=en_comm
    return res

print(citation_en_commun())
  ######################################CREATION DES GRAPHES     
def create_gephi_graph(graph: dict, auteur_dict: dict, auteur_cible: str, file_name: str):
    G = nx.Graph()
    #print(auteur_dict)
    # Ajoute toutes les arêtes
    for source, voisins in graph.items():
        for target in voisins:
            G.add_edge(source, target)

    # Ajoute les attributs aux nœuds
    for node in G.nodes:
        auteurs = auteur_dict.get(node, "")
        titre = id_to_title(node)
        cible = "oui" if auteur_cible.lower() in auteurs.lower() else "non"

        G.nodes[node]['auteurs'] = auteurs
        G.nodes[node]['auteur_cible'] = cible
        G.nodes[node]['label'] = titre  # Le titre est l'étiquette visible dans Gephi

        if cible == "oui":
            G.nodes[node]['viz'] = {'color': {'r': 255, 'g': 80, 'b': 80, 'a': 1.0}}
        else:
            G.nodes[node]['viz'] = {'color': {'r': 180, 'g': 180, 'b': 180, 'a': 0.7}}

    nx.write_gexf(G, f"graphes/{file_name}.gexf")


def create_gephi_graph_2(graph: dict, auteur_dict: dict, keywords_dict: dict,auteurs_cible: list, keywords_cible: list, file_name: str):
    G = nx.Graph()
    #print(auteur_dict)
    # Ajoute toutes les arêtes

    for source, voisins in graph.items():
        for target in voisins:
            G.add_edge(source, target)
    for node_id in dico.keys():
        node_label = node_id
        if node_label not in G and afficher_noeud_isole:
            G.add_node(node_label)
    taille = 0
    # Ajoute les attributs aux nœuds
    for node in G.nodes:
        auteurs = auteur_dict.get(node, "")
        #print(auteurs)
        keywords = keywords_dict.get(node, "")
        titre = id_to_title(node)
        cible= "non"

        for noms in auteurs_cible :
            if noms.lower() in auteurs.lower() :
                taille +=1
                cible = "oui"
        if(auteurs_cible==[] and not filtrage_union):
            cible = "oui"
        for words in keywords_cible :
            if (not filtrage_union):
                if cible == "oui" :
                    if words.lower() not in keywords.lower() :
                        cible = "non"
            else:
                if words.lower() in keywords.lower() :
                        cible = "oui"
        #print(cible)
        G.nodes[node]['auteurs'] = auteurs
        G.nodes[node]['mots-clefs'] = keywords
        G.nodes[node]['cible'] = cible
        G.nodes[node]['label'] = titre  # Le titre est l'étiquette visible dans Gephi
        if article_permanent(auteurs):
            G.nodes[node]['viz'] = {'color': {'r': 255, 'g': 80, 'b': 255, 'a': 1.0}}
        elif cible == "oui":
            G.nodes[node]['viz'] = {'color': {'r': 255, 'g': 80, 'b': 80, 'a': 1.0}}
        else:
            G.nodes[node]['viz'] = {'color': {'r': 180, 'g': 180, 'b': 180, 'a': 0.7}}
    print(taille)
    nx.write_gexf(G, f"graphes/{file_name}.gexf")


############################# GRAPH ######################################

def create_gephi_graph_bert(seuil, auteur_dict: dict, keywords_dict: dict,auteurs_cible: list, keywords_cible: list, file_name: str):
    G = nx.Graph()
    #print(auteur_dict)
    # Ajoute toutes les arêtes
      # 1. Extraire les titres
    ids = list(dico.keys())
    titres = [dico[i]['title'] for i in ids]
    print(ids)

    # 2. Embedding des titres
    embeddings = model.encode(titres, convert_to_numpy=True)

    # 3. Similarité cosinus
    sim_matrix = cosine_similarity(embeddings)
    
    # 4. Création du graphe
    graph = {dico_id: [] for dico_id in ids}

    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            if sim_matrix[i][j] >= seuil:
                graph[ids[i]].append(ids[j])
                graph[ids[j]].append(ids[i])  # symétrique

    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            sim = sim_matrix[i][j]
            if sim > 0.6:  # seuil
                G.add_edge(ids[i], ids[j], weight=sim)
            else:
                G.add_edge(ids[i], ids[j], weight=0.01)
  
    # Layout avec positions influencées par la similarité (poids)
    pos = nx.spring_layout(G, weight='weight', seed=42)
    threshold = 0.6
    G_strong = nx.Graph()
    for u, v, data in G.edges(data=True):
        if data['weight'] >= threshold:
            G_strong.add_edge(u, v, weight=data['weight'])
    for node_id in dico.keys():
        node_label = node_id
        if node_label not in G and afficher_noeud_isole:
            G_strong.add_node(node_label)

    # Ajouter les positions et labels
    for n in G_strong.nodes:
        G_strong.nodes[n]['pos'] = pos[n]

    # Affichage
    for node in G_strong.nodes:
        auteurs = auteur_dict.get(node, "")
        keywords = keywords_dict.get(node, "")
        titre = id_to_title(node)
        cible= "non"
        for noms in auteurs_cible :
            if noms.lower() in auteurs.lower() :
   
                cible = "oui"
        if(auteurs_cible==[] and not filtrage_union):
            cible = "oui"
        for words in keywords_cible :
            if (not filtrage_union):
                if cible == "oui" :
                    if words.lower() not in keywords.lower() :
                        cible = "non"
            else:
                if words.lower() in keywords.lower() :
                        cible = "oui"
        #print(cible)
        G_strong.nodes[node]['auteurs'] = auteurs
        G_strong.nodes[node]['mots-clefs'] = keywords
        G_strong.nodes[node]['cible'] = cible
        if(cible=="non") and not afficher_non_cible:
            G_strong.nodes[node]['label'] = "" 
        else:
            G_strong.nodes[node]['label'] = titre  # Le titre est l'étiquette visible dans Gephi
    edge_colors = []
    for u, v in G_strong.edges():
        if (G_strong.nodes[u].get('cible') == 'oui') and (G_strong.nodes[v].get('cible') == 'oui') and colorien_lien:
            edge_colors.append('red')  # lien entre deux cibles
        else:
            edge_colors.append('gray')  # lien normal
    # Récupérer les labels (par exemple depuis l'attribut "label")
    labels = {node: data.get('label', node) for node, data in G_strong.nodes(data=True)}
    colors = []
    for node in G_strong.nodes(data=True):
        if node[1].get('cible') == 'oui' and (auteur_cibles!=[] or keyword_cibles!=[]): 
                
            colors.append('tomato')
        elif article_permanent(node[1]['auteurs']):
            colors.append('plum')
            if node[1].get('cible') != 'oui' and not afficher_non_cible: 
                node[1]['label']= ""
    
        else:
            if not afficher_non_cible:
                node[1]['label']= " "
            colors.append('lightgray')

    # Dessin du graphe
    plt.figure(figsize=(12, 12))
    
    nx.draw_networkx_nodes(G_strong, pos, node_color=colors, node_size=300)
    nx.draw_networkx_edges(G_strong, pos, edge_color=edge_colors, alpha=0.5)
    nx.draw_networkx_labels(G_strong, pos, labels=labels, font_size=6, font_color='black')


    legend_elements = [
        mpatches.Patch(color='tomato', label='Nœud avec ces auteurs : [' + ";".join(auteurs_cible) +"]\n et ces mots clefs : ["+ ";".join(keywords_cible)+"]"),
        mpatches.Patch(color='plum', label='Nœud auteur permanent'),
        mpatches.Patch(color='lightgray', label='Nœud autre'),
        mlines.Line2D([], [], color='red', linewidth=2, label='Lien entre cibles'),
        mlines.Line2D([], [], color='gray', linewidth=2, label='Lien autre')
    ]

    plt.legend(handles=legend_elements, loc='lower left', fontsize=10, frameon=True)

    plt.axis('off')
    plt.tight_layout()
    plt.savefig("graphes/graph_image_labels.png", dpi=300)
    plt.show()


        
fichier_gexf = "fichier_de_test"
auteur_cibles = []
keyword_cibles= []          
create_gephi_graph_bert(0.6,author_dic(dico),keywords_dic(dico),auteur_cibles,keyword_cibles,fichier_gexf)
    

#########################################################################
def create_gephi_graph_authors(graph: dict, auteur_dict: dict, keywords_dict: dict,auteurs_cible: list, keywords_cible: list, file_name: str):
    G = nx.Graph()
    #print(auteur_dict)
    # Ajoute toutes les arêtes
    for source, voisins in graph.items():
        for target in voisins:
            G.add_edge(source, target)

    # Ajoute les attributs aux nœuds
    for node in G.nodes:
        auteurs = auteur_dict.get(node, "")
        keywords = keywords_dict.get(node, "")
        cible= "non"
        
        for noms in auteurs_cible :
            if noms in node :
                cible = "oui"

            elif colorier_voisin:
                for elt in graph[node]:
                    if noms.lower() in elt.lower():
                        cible = "oui"
        if(auteurs_cible==[]):
            cible = "oui"
        for words in keywords_cible :
            if cible == "oui" :
                if all(words.lower() not in elt.lower() for elt in  keywords_dic_authors[node]):
                    cible = "non"
        G.nodes[node]['auteurs'] = node
        G.nodes[node]['mots-clefs'] = keywords
        G.nodes[node]['cible'] = cible
        G.nodes[node]['label'] = node  # Le titre est l'étiquette visible dans Gephi

        if cible == "oui":
            G.nodes[node]['viz'] = {'color': {'r': 255, 'g': 80, 'b': 80, 'a': 1.0}}
        else:
            G.nodes[node]['viz'] = {'color': {'r': 180, 'g': 180, 'b': 180, 'a': 0.7}}
     

    nx.write_gexf(G, f"graphes/{file_name}.gexf")

'''#print(transfo((generate_graph_topic())))
#print(len(transfo((generate_graph_topic())).keys()))
fichier_gexf = "fichier_de_test"
auteur_cibles = ["Labeau","Chloé  Clavel","brian"]
keyword_cibles= []
#create_gephi_graph_authors(((generate_graph_authors_sametheme())),author_dic(dico),keywords_dic(dico),auteur_cibles,keyword_cibles,fichier_gexf)
#create_gephi_graph_2(citation_en_commun(),author_dic(dico),keywords_dic(dico),auteur_cibles,keyword_cibles,fichier_gexf)
#create_gephi_graph_2(((generate_graph_topic())),author_dic(dico),keywords_dic(dico),auteur_cibles,keyword_cibles,fichier_gexf)
create_gephi_graph_2(generate_graph_title_similarity(dico),author_dic(dico),keywords_dic(dico),auteur_cibles,keyword_cibles,fichier_gexf)
#create_gephi_graph_2(((generate_graph_authors())),author_dic(dico),keywords_dic(dico),auteur_cibles,[],fichier_gexf)

#write_to_file(transfo (generate_graph_topic()),"topic_common_new") # A l'ancienne
#write_to_file(transfo (generate_graph_authors()),"author_common_new")
def ouvrir_gephi(fichier_gexf):
    chemin_gephi = "/Applications/Gephi.app/Contents/MacOS/Gephi"
    subprocess.run([chemin_gephi, "graphes/"+fichier_gexf +".gexf" ])

#ouvrir_gephi(fichier_gexf)

G = nx.read_gexf("graphes/"+fichier_gexf +".gexf")
# Création d'une disposition (ex: spring layout)
pos = nx.spring_layout(G, seed=42, k=0.5)

# Définir les couleurs à partir de l'attribut 'auteur_cible'
colors = []
for node in G.nodes(data=True):
    if node[1].get('cible') == 'oui':     
        colors.append('tomato')
    elif article_permanent(node[1]['auteurs']):
        colors.append('plum')
        if node[1].get('cible') != 'oui' and not afficher_non_cible: 
            node[1]['label']= ""
   
    else:
        if not afficher_non_cible:
            node[1]['label']= ""
        colors.append('lightgray')

edge_colors = []
for u, v in G.edges():
    if (G.nodes[u].get('cible') == 'oui') and (G.nodes[v].get('cible') == 'oui') and colorien_lien:
        edge_colors.append('red')  # lien entre deux cibles
    else:
        edge_colors.append('gray')  # lien normal
# Récupérer les labels (par exemple depuis l'attribut "label")
labels = {node: data.get('label', node) for node, data in G.nodes(data=True)}

# Dessin du graphe
plt.figure(figsize=(12, 12))
nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=300)
nx.draw_networkx_edges(G, pos, edge_color=edge_colors, alpha=0.5)
nx.draw_networkx_labels(G, pos, labels=labels, font_size=6, font_color='black')


legend_elements = [
    mpatches.Patch(color='tomato', label='Nœud avec ces auteurs : [' + ";".join(auteur_cibles) +"]\n et ces mots clefs : ["+ ";".join(keyword_cibles)+"]"),
    mpatches.Patch(color='plum', label='Nœud auteur permanent'),
    mpatches.Patch(color='lightgray', label='Nœud autre'),
    mlines.Line2D([], [], color='red', linewidth=2, label='Lien entre cibles'),
    mlines.Line2D([], [], color='gray', linewidth=2, label='Lien autre')
]

plt.legend(handles=legend_elements, loc='lower left', fontsize=10, frameon=True)

plt.axis('off')
plt.tight_layout()
plt.savefig("graphes/graph_image_labels.png", dpi=300)
plt.show()'''