import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import nltk

# Télécharger les stopwords français
nltk.download('stopwords')
stop_words = stopwords.words('french')

# Exemple de corpus de documents
corpus = [
    "Le machine learning est une discipline passionnante.",
    "L'apprentissage automatique permet de faire des prédictions.",
    "Les techniques de visualisation aident à comprendre les données.",
    "Le deep learning permet de traiter de grandes quantités de données."
]

# 1. Extraction des mots-clés avec TF-IDF
vectorizer = TfidfVectorizer(stop_words=stop_words)
tfidf_matrix = vectorizer.fit_transform(corpus)
terms = vectorizer.get_feature_names_out()

# 2. Calcul de la similarité entre les termes
similarity_matrix = cosine_similarity(tfidf_matrix.T)

# 3. Construction du graphe de thèmes
seuil = 0.1  # Seuil de similarité pour créer une arête
G = nx.Graph()

# Ajout des nœuds
for term in terms:
    G.add_node(term)

# Ajout des arêtes en fonction de la similarité
for i in range(len(terms)):
    for j in range(i + 1, len(terms)):
        if similarity_matrix[i, j] > seuil:
            G.add_edge(terms[i], terms[j], weight=similarity_matrix[i, j])

# 4. Visualisation du graphe
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G, seed=42)
edges = G.edges(data=True)
weights = [d['weight'] for (_, _, d) in edges]

# Dessin des nœuds
nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=600)
# Dessin des arêtes avec une épaisseur proportionnelle au poids
nx.draw_networkx_edges(G, pos, width=[w * 5 for w in weights])
# Ajout des étiquettes
nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")

plt.title("Graphe de thèmes basé sur la similarité TF-IDF")
plt.axis("off")
plt.show()
