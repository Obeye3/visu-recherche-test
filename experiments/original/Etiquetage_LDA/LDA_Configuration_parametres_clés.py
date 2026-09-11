from etiquetage_articles_permanents import main
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




def visualisation(num_topics=12):

    results = main(num_topics)

    lda = results['lda']
    corpus = results['corpus']
    dictionary = results['dictionary']

    vis_data = gensimvis.prepare(lda, corpus, dictionary)
    pyLDAvis.save_html(vis_data, f'lda_visualisation__{num_topics}.html')

def score_coherence():
    for num_topics in range(2, 21, 2):
        print(f'\nCalculating coherence score for {num_topics} topics...')
        results = main(num_topics)

        lda = results['lda']
        corpus = results['corpus']
        dictionary = results['dictionary']

        coherence_model_lda = CoherenceModel(model=lda, texts=results['documents'], dictionary=dictionary, coherence='c_v')
        coherence_lda = coherence_model_lda.get_coherence()
        print(f'\nCoherence Score for {num_topics} topics: ', coherence_lda)
  


if __name__ == "__main__":
    visualisation(num_topics=12)

