from prince import CA
import matplotlib.pyplot as plt
from gensim import corpora, models
from gensim.utils import simple_preprocess
import os
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from langdetect import detect
import matplotlib.pyplot as plt
from gensim.models import LdaModel
from gensim.corpora import Dictionary
from gensim.models.coherencemodel import CoherenceModel
import re
from codecarbon import EmissionsTracker

tracker = EmissionsTracker()
tracker.start()

# ton code ici



def supprimer_stopwords(texte, langue='english'):
    mots = word_tokenize(texte)
    stop_words = set(stopwords.words(langue))
    mots_filtrés = [mot for mot in mots if mot.lower() not in stop_words]
    return ' '.join(mots_filtrés)

if __name__ == '__main__':
    # Chargement du fichier
    with open("../web_scraping/s2a_thèses_1.txt", 'r', encoding='utf-8') as file:
        contenu = file.read()

    # Séparation des documents
    pattern = re.findall(
    r"Thèse\s*(\d+)\s*:(.*?)\s*(?:@members:\s*(.*?))?(?=\s+Thèse|\Z)", 
    contenu, 
    re.DOTALL)

    # Formatage en liste de dictionnaires
    theses = []
    for num, title, members in pattern:
        theses.append({
        "numero": int(num),
        "titre": title.strip(),
        "membres": [m.strip() for m in members.split(",")] if members else []
        })

    
    # Prétraitement
    documents = [thèse['titre'] for thèse in theses]
    membres = [thèse['membres'] for thèse in theses]
    print(membres[:5])
    print(documents[:5])
    texts = [
        simple_preprocess(supprimer_stopwords(doc))
        for doc in documents
    ]

    # Dictionnaire et corpus
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

'''
    # Calcul des scores de cohérence
    coherence_scores = []
    topic_range = range(5,20)


    for num_topics in topic_range:
        lda_model = LdaModel(corpus=corpus,
                             id2word=dictionary,
                             num_topics=num_topics,
                             random_state=42,
                             passes=10,
                             iterations=100)
        
        coherence_model = CoherenceModel(model=lda_model, texts=texts, dictionary=dictionary, coherence='c_v')
        score = coherence_model.get_coherence()
        coherence_scores.append(score)
        print(f"Topics: {num_topics} | Cohérence: {score:.4f}")

    # Tracer la courbe
    plt.plot(topic_range, coherence_scores, marker='o')
    plt.xlabel('Nombre de topics')
    plt.ylabel('Score de cohérence (c_v)')
    plt.title('Cohérence vs Nombre de topics')
    plt.grid(True)
    plt.show()


'''
# 4. Entraînement du modèle LDA pour assigner à chaque document un topic dominant

num_topics = 12  # Choisissez le nombre de topics que vous souhaitez

lda_model = LdaModel(corpus=corpus,
                             id2word=dictionary,
                             num_topics=num_topics,
                             random_state=42,
                             passes=10,
                             iterations=100)

L = [0]

for bow in corpus:
    topic_distribution = lda_model.get_document_topics(bow)
    # Récupère le topic avec la plus haute probabilité
    dominant_topic = max(topic_distribution, key=lambda x: x[1])[0]
    L.append(dominant_topic)


print(L[:5])
"""

# Affichage des topics pour un numbre de topics donné
lda_model = models.LdaModel(corpus=corpus,
                            id2word=dictionary,
                            num_topics=13,
                            random_state=42,
                            passes=10,
                            alpha='auto',
                            eta='auto')


vis_data = gensimvis.prepare(lda_model, corpus, dictionary)

pyLDAvis.save_html(vis_data, 'lda_visualisation_13.html')
"""

#Tableau de contingence : 
import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns


# Accumulateur (membre → topic → somme)
acc = defaultdict(lambda: defaultdict(float))

# Remplissage : on ajoute le coefficient du membre pour le topic assigné à chaque doc
for doc_id, topic_id in enumerate(L[1:]):
    for membre in membres[doc_id]:
        acc[membre][topic_id] += 1

acc_filtered = {membre: topics for membre, topics in acc.items() if len(topics) > 5}
print(acc_filtered)
    
# Transformation en DataFrame
df = pd.DataFrame.from_dict(acc_filtered, orient='index').fillna(0).sort_index()
df.columns.name = 'Topic'
df.index.name = 'Membre'
# Ajuster les options d'affichage pour montrer toutes les lignes et colonnes
pd.set_option('display.max_rows', None)  # Afficher toutes les lignes
pd.set_option('display.max_columns', None)  # Afficher toutes les colonnes
pd.set_option('display.width', None)  # Pas de limite de largeur
pd.set_option('display.max_colwidth', None)  # Pas de limite de largeur des colonnes

# Afficher la table complète de contingence

print(df)
'''
import matplotlib.pyplot as plt
import seaborn as sns
# Affichage du premier histogramme: Membres par Topic
topic_counts = df.sum(axis=0)  # Somme des coefficients par topic, représentant le nombre de membres par topic
plt.figure(figsize=(10, 6))
sns.barplot(x=topic_counts.index, y=topic_counts.values, palette='viridis')
plt.title('Histogramme : Nombre de Membres par Topic')
plt.xlabel('Topic')
plt.ylabel('Nombre de Membres')
plt.show()
'''
# Affichage du deuxième histogramme: Topics par Membre


# Étape 1 : S'assurer que les index/colonnes sont bien nommés
df.index.name = 'Auteur'
df.columns.name = 'Topic'

# Étape 2 : Lancer l'AFC
ca = CA(n_components=2, random_state=42)
ca = ca.fit(df)

# Étape 3 : Extraire les coordonnées
row_coords = ca.row_coordinates(df)
col_coords = ca.column_coordinates(df)

# Étape 4 : Visualiser les résultats
plt.figure(figsize=(20, 12))

# Auteurs (lignes)
plt.scatter(row_coords[0], row_coords[1], color='blue', label='Auteurs')
for i, label in enumerate(df.index):
    plt.text(row_coords.iloc[i, 0], row_coords.iloc[i, 1], label, fontsize=9, color='blue')

# Topics (colonnes)
plt.scatter(col_coords[0], col_coords[1], color='red', marker='x', label='Topics')
for i, label in enumerate(df.columns):
    plt.text(col_coords.iloc[i, 0], col_coords.iloc[i, 1], f'Topic {label}', fontsize=9, color='red')

# Axes
plt.axhline(0, color='gray', linestyle='--')
plt.axvline(0, color='gray', linestyle='--')
plt.xlabel('Dimension 1')
plt.ylabel('Dimension 2')
plt.title('Analyse Factorielle des Correspondances (AFC)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
emissions = tracker.stop()
print(f"Émissions estimées : {emissions:.6f} kg de CO₂")
