from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Télécharger les ressources nécessaires
nltk.download("punkt")
nltk.download("stopwords")

def extract_topics(text, num_topics=5, num_words=5):
    stop_words = set(stopwords.words("english"))
    
    # Tokenisation et filtrage des stopwords
    words = word_tokenize(text.lower())
    filtered_text = " ".join([word for word in words if word.isalnum() and word not in stop_words])
    
    # Vectorisation TF-IDF
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform([filtered_text])
    
    # Modèle LDA pour extraire les thèmes
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda.fit(X)
    
    feature_names = vectorizer.get_feature_names_out()
    topics = {}
    
    for topic_idx, topic in enumerate(lda.components_):
        topic_words = [feature_names[i] for i in topic.argsort()[:-num_words - 1:-1]]
        topic_title = " ".join(topic_words[:3])  # Utilisation des 3 premiers mots pour donner un titre
        topics[f"{topic_title}"] = topic_words
    
    return topics

def plot_topic_graph(topics):
    G = nx.Graph()
    
    for topic, words in topics.items():
        G.add_node(topic, color='red')
        for word in words:
            G.add_node(word, color='blue')
            G.add_edge(topic, word)
    
    colors = [G.nodes[node]['color'] for node in G.nodes]
    
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color=colors, edge_color='gray', node_size=2000, font_size=10)
    plt.title("Graph of Extracted Topics")
    plt.show()

# Exemple d'utilisation
text = """Illustrations of
the test-time predictions on a Mixture of three Gaussians (green points) with 49 hypotheses. Shaded
blue circles represent the hypothesis predictions, with intensity corresponding to the predicted scores.
(Left) Predictions of MCL as proposed in [ 41, 42 ]. (Middle) Predictions of Relaxed WTA [63] with
ε = 0.1. (Right) Annealed MCL with initial temperature T0 = 0.6. Each model was trained with
the same backbone (a three-layer MLP). We see that WTA leaves out some hypotheses, achieving
a higher quantization error than aMCL. Moreover, we see that Relaxed-WTA is biased toward the
barycenter of the distribution, in contrast with aMCL.
Therefore, at the lowest level, aMCL simply consists of replacing the min operator from (2) by
softmin. aMCL introduces the temperature schedule as an additional hyperparameter. As highlighted
by the literature on simulated annealing [ 26], it is crucial to ensure that the temperature decreases
slowly enough to benefit from the advantages of annealing. In practice, we experimented with both
linear and exponential schedulers (see also Section 5).
On a higher level, we can interpret the objective of aMCL as a smoothed version of the MCL objective.
Smoothing with high temperature simplifies the optimization problem (6), making the loss landscape
easier to navigate: we can conjecture from this analysis that aMCL will find a global minimum at
high temperature, and we can expect it to stay optimal as long as the temperature decreases slowly
enough [ 9 ]. We can also see aMCL as an input-dependent version of deterministic annealing [61 , 62].
In this view, a high temperature encourages the exploration of the hypothesis space and mitigates
the greediness of the gradient descent update (3). Moreover, following [ 26 ], we can posit that there
exists an optimal temperature schedule striking a balance between exploration and optimization. Yet
another interpretation is that aMCL constitutes an adaptative extension of Relaxed-MCL [ 63 ], as
qT (t)(fk | x, y) depends both on the distance between the hypothesis fk(x) and the target y, and
the training step t. These interpretations shed light on the inner workings of aMCL. However, the
complete training dynamic of the algorithm appears when we analyze aMCL through the lens of
information theory and statistical physics, which is the purpose of the next section.."""

extracted_topics = extract_topics(text)
plot_topic_graph(extracted_topics)
