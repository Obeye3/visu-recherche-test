# -*- coding: utf-8 -*-
"""
Visualisation NLP Avancée avec Dash - Analyse des Topics et Auteurs
Fonctionnalités:
- Support multilingue (français/anglais)
- Exclusion des noms d'auteurs des mots-clés
- Hover avec top auteurs par topic
- Recherche inverse: topics par auteur
"""

import numpy as np
import pandas as pd
import re
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Set
import unicodedata

# ML et NLP
from sentence_transformers import SentenceTransformer
import umap
import hdbscan
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
from sklearn.manifold import MDS
from bertopic import BERTopic

# Visualisation
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Dash
import dash
from dash import dcc, html, Input, Output, State, callback_context
import webbrowser
from threading import Timer

class AdvancedNLPProcessor:
    """Processeur NLP avancé pour l'analyse des topics et auteurs"""
    
    def __init__(self):
        self.documents = []
        self.metadata = []
        self.authors_set = set()
        self.topic_model = None
        self.topics = None
        self.embeddings = None
        self.topic_data = {}
        self.author_contributions = {}
        self.author_to_topics = defaultdict(list)
        
    def parse_enriched_file(self, filename: str) -> bool:
        """Parse le fichier enrichi avec titres, auteurs, abstracts, etc."""
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            print(f"❌ Fichier '{filename}' non trouvé")
            return False
        
        print(f"📁 Lecture du fichier: {len(content)} caractères")
        
        # Séparer les articles par le séparateur
        articles = content.split("=" * 80)
        articles = [art.strip() for art in articles if art.strip()]
        
        print(f"📊 {len(articles)} articles trouvés")
        
        # Réinitialiser les listes pour éviter les doublons
        self.documents = []
        self.metadata = []
        self.authors_set = set()
        
        for i, article in enumerate(articles):
            metadata = self._parse_single_article(article, i)
            if metadata:
                # Combiner titre et abstract pour BERTopic
                combined_text = f"{metadata['title']} {metadata['abstract']}"
                
                # Vérifier que le texte est suffisant
                if len(combined_text.strip()) > 50:
                    self.documents.append(combined_text)
                    self.metadata.append(metadata)
                    
                    # Collecter tous les auteurs
                    if metadata['authors']:
                        for author in metadata['authors']:
                            self.authors_set.add(author.strip())
                else:
                    print(f"⚠️  Article {i} ignoré: texte trop court")
        
        print(f"✅ {len(self.documents)} documents parsés")
        print(f"👥 {len(self.authors_set)} auteurs uniques trouvés")
        
        if len(self.documents) < 2:
            print("❌ Pas assez de documents pour BERTopic")
            return False
            
        return True
    
    def _parse_single_article(self, article: str, index: int) -> Dict:
        """Parse un seul article et extrait ses métadonnées"""
        
        metadata = {
            'index': index,
            'article_num': '',
            'title': '',
            'hal_id': '',
            'authors': [],
            'year': '',
            'type': '',
            'keywords': [],
            'abstract': ''
        }
        
        lines = article.split('\n')
        current_section = None
        abstract_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Identifier les sections
            if line.startswith('Article '):
                metadata['article_num'] = line.replace('Article ', '').strip()
            elif line.startswith('TITRE :'):
                metadata['title'] = line.replace('TITRE :', '').strip()
            elif line.startswith('HAL ID :'):
                metadata['hal_id'] = line.replace('HAL ID :', '').strip()
            elif line.startswith('AUTEURS :'):
                authors_str = line.replace('AUTEURS :', '').strip()
                metadata['authors'] = self._parse_authors(authors_str)
            elif line.startswith('ANNÉE :'):
                metadata['year'] = line.replace('ANNÉE :', '').strip()
            elif line.startswith('TYPE :'):
                metadata['type'] = line.replace('TYPE :', '').strip()
            elif line.startswith('MOTS-CLÉS :'):
                keywords_str = line.replace('MOTS-CLÉS :', '').strip()
                metadata['keywords'] = [k.strip() for k in keywords_str.split(';') if k.strip()]
            elif line.startswith('ABSTRACT :'):
                current_section = 'abstract'
            elif current_section == 'abstract':
                abstract_lines.append(line)
        
        metadata['abstract'] = ' '.join(abstract_lines).strip()
        
        # Validation
        if not metadata['abstract'] or len(metadata['abstract']) < 50:
            return None
            
        return metadata
    
    def _parse_authors(self, authors_str: str) -> List[str]:
        """Parse la chaîne d'auteurs et retourne une liste nettoyée"""
        
        authors = []
        
        # Nettoyer la chaîne d'abord
        authors_str = authors_str.replace('\n', ' ')
        
        # Essayer différents séparateurs
        separators = [',', ';', ' and ', ' et ', '\n']
        current_list = [authors_str]
        
        for sep in separators:
            new_list = []
            for item in current_list:
                new_list.extend(item.split(sep))
            current_list = new_list
        
        for author in current_list:
            author = author.strip()
            # Nettoyer les caractères spéciaux et normaliser
            author = unicodedata.normalize('NFKD', author)
            # Supprimer les emails
            author = re.sub(r'\S+@\S+', '', author)
            # Supprimer les affiliations en chiffres
            author = re.sub(r'\d+', '', author)
            # Nettoyer les espaces multiples
            author = re.sub(r'\s+', ' ', author).strip()
            
            # Vérifier que l'auteur est valide
            if author and len(author) > 3 and not re.match(r'^[^a-zA-Z]*$', author):
                # L'auteur doit contenir au moins quelques lettres
                if re.search(r'[a-zA-Z]', author):
                    authors.append(author)
        
        return authors
    
    def _create_comprehensive_stopwords(self) -> List[str]:
        """Crée une liste complète de stopwords incluant tous les auteurs"""
        
        # Stopwords de base
        base_stopwords = list(text.ENGLISH_STOP_WORDS.union([
            # Français
            'le', 'la', 'les', 'de', 'des', 'du', 'un', 'une', 'et', 'en', 'dans', 'au', 'aux', 'ce', 'ces', 'ça',
            'pour', 'pas', 'par', 'sur', 'se', 'plus', 'ou', 'avec', 'tout', 'mais', 'comme', 'si', 'sans', 'être',
            'cette', 'son', 'sa', 'ses', 'on', 'il', 'elle', 'ils', 'elles', 'nous', 'vous', 'je', 'tu', 'mon', 'ma',
            'mes', 'ton', 'ta', 'tes', 'notre', 'nos', 'votre', 'vos', 'leur', 'leurs', 'y', 'donc',
            
            # Termes académiques
            'abstract', 'introduction', 'conclusion', 'references', 'bibliography', 'acknowledgments', 'appendix',
            'figure', 'table', 'section', 'chapter', 'paper', 'article', 'conference', 'journal', 'proceedings',
            'isbn', 'doi', 'arxiv', 'hal', 'submitted', 'published', 'author', 'authors', 'corresponding',
            'email', 'telecom', 'paris', 'institute', 'university', 'université', 'laboratoire', 'laboratory', 
            'team', 'cite', 'version', 'al', 'pp', 'vol', 'no', 'page', 'pages', 'ltci', 'polytechnique',
            
            # Mots techniques génériques
            'method', 'approach', 'technique', 'algorithm', 'model', 'framework', 'system', 'analysis',
            'evaluation', 'experiment', 'result', 'performance', 'comparison', 'study', 'research',
            'méthode', 'approche', 'technique', 'algorithme', 'modèle', 'système', 'analyse', 'évaluation',
            'expérience', 'résultat', 'performance', 'comparaison', 'étude', 'recherche'
        ]))
        
        # Ajouter tous les noms d'auteurs (nom et prénom séparément)
        author_words = set()
        for author in self.authors_set:
            # Séparer les mots du nom complet
            words = re.findall(r'\w+', author.lower())
            for word in words:
                if len(word) > 2:  # Ignorer les initiales
                    author_words.add(word)
        
        print(f"📝 Stopwords créés: {len(base_stopwords)} de base + {len(author_words)} noms d'auteurs")
        
        return base_stopwords + list(author_words)
    
    def train_topic_model(self) -> bool:
        """Entraîne le modèle BERTopic multilingue"""
        
        if not self.documents:
            print("❌ Aucun document à traiter")
            return False
        
        print(f"🤖 Entraînement BERTopic sur {len(self.documents)} documents...")
        
        # Modèle d'embedding multilingue
        embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        
        # UMAP pour la réduction dimensionnelle - paramètres ajustés
        n_neighbors = min(15, max(2, len(self.documents) - 1))
        umap_model = umap.UMAP(
            n_neighbors=n_neighbors,
            n_components=5,
            min_dist=0.0,
            metric='cosine',
            random_state=42
        )
        
        # HDBSCAN pour le clustering - paramètres plus robustes
        min_cluster_size = max(2, min(10, len(self.documents) // 15))
        hdbscan_model = hdbscan.HDBSCAN(
            min_cluster_size=min_cluster_size,
            min_samples=1,
            metric='euclidean',
            cluster_selection_method='eom'
        )
        
        # Vectorizer avec stopwords complets
        custom_stopwords = self._create_comprehensive_stopwords()
        vectorizer_model = TfidfVectorizer(
            stop_words=custom_stopwords,
            max_features=1000,
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95
        )
        
        print(f"📊 Paramètres HDBSCAN: min_cluster_size={min_cluster_size}, n_neighbors={n_neighbors}")
        
        # Modèle BERTopic
        self.topic_model = BERTopic(
            embedding_model=embedding_model,
            umap_model=umap_model,
            hdbscan_model=hdbscan_model,
            vectorizer_model=vectorizer_model,
            language="multilingual",
            verbose=True
        )
        
        try:
            # Entraînement
            self.topics, _ = self.topic_model.fit_transform(self.documents)
            
            # Calcul des embeddings pour la visualisation
            self.embeddings = embedding_model.encode(self.documents)
            
            # Vérifier que le clustering a fonctionné
            unique_topics = set(self.topics)
            n_clusters = len(unique_topics) - (1 if -1 in unique_topics else 0)
            n_outliers = self.topics.count(-1) if -1 in self.topics else 0
            
            print(f"✅ Clustering terminé:")
            print(f"   - Topics trouvés: {n_clusters}")
            print(f"   - Documents outliers: {n_outliers}")
            print(f"   - Topics: {sorted(unique_topics)}")
            
            if n_clusters < 2:
                print("⚠️  Très peu de clusters trouvés, ajustement des paramètres...")
                return self._retry_with_adjusted_parameters()
            
            # Analyse des topics
            self._analyze_topics()
            self._calculate_author_contributions()
            
            print(f"✅ Modèle entraîné avec succès!")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de l'entraînement: {e}")
            print("🔄 Tentative avec paramètres alternatifs...")
            return self._retry_with_adjusted_parameters()
    
    def _retry_with_adjusted_parameters(self) -> bool:
        """Réessaie avec des paramètres plus conservateurs"""
        
        print("🔄 Retry avec paramètres ajustés...")
        
        # Paramètres très conservateurs
        embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        
        # UMAP plus conservateur
        umap_model = umap.UMAP(
            n_neighbors=5,
            n_components=2,
            min_dist=0.1,
            metric='cosine',
            random_state=42
        )
        
        # HDBSCAN plus permissif
        hdbscan_model = hdbscan.HDBSCAN(
            min_cluster_size=2,
            min_samples=1,
            metric='euclidean',
            cluster_selection_method='eom'
        )
        
        # Vectorizer simplifié
        custom_stopwords = self._create_comprehensive_stopwords()
        vectorizer_model = TfidfVectorizer(
            stop_words=custom_stopwords,
            max_features=500,
            ngram_range=(1, 1),
            min_df=1,
            max_df=0.9
        )
        
        # Modèle BERTopic simplifié
        self.topic_model = BERTopic(
            embedding_model=embedding_model,
            umap_model=umap_model,
            hdbscan_model=hdbscan_model,
            vectorizer_model=vectorizer_model,
            language="multilingual",
            verbose=True
        )
        
        try:
            self.topics, _ = self.topic_model.fit_transform(self.documents)
            self.embeddings = embedding_model.encode(self.documents)
            
            # Vérification
            unique_topics = set(self.topics)
            n_clusters = len(unique_topics) - (1 if -1 in unique_topics else 0)
            
            print(f"✅ Retry réussi: {n_clusters} topics trouvés")
            
            if n_clusters >= 1:
                self._analyze_topics()
                self._calculate_author_contributions()
                return True
            else:
                print("❌ Retry échoué aussi")
                return False
                
        except Exception as e:
            print(f"❌ Retry échoué: {e}")
            return False
    
    def _analyze_topics(self):
        """Analyse les topics et calcule les positions 2D"""
        
        topic_info = self.topic_model.get_topic_info()
        
        # Calculer les positions 2D des topics
        topic_coords = self._calculate_topic_positions()
        
        print(f"📊 Analyse de {len(topic_info)} topics...")
        
        for _, row in topic_info.iterrows():
            topic_id = row['Topic']
            if topic_id == -1:  # Ignorer les outliers
                continue
            
            topic_words = self.topic_model.get_topic(topic_id)
            coords = topic_coords.get(topic_id, {'x': 0, 'y': 0})
            
            self.topic_data[topic_id] = {
                'id': topic_id,
                'size': row['Count'],
                'x': coords['x'],
                'y': coords['y'],
                'words': [word for word, score in topic_words[:10]],
                'scores': [score for word, score in topic_words[:10]],
                'keywords_str': ', '.join([word for word, score in topic_words[:5]]),
                'documents': [i for i, t in enumerate(self.topics) if t == topic_id]
            }
            
            print(f"✅ Topic {topic_id}: {row['Count']} docs, mots-clés: {', '.join([word for word, score in topic_words[:3]])}")
        
        print(f"📈 Total: {len(self.topic_data)} topics analysés")
    
    def _calculate_topic_positions(self) -> Dict:
        """Calcule les positions 2D des topics avec MDS"""
        
        topic_embeddings = {}
        
        for topic_id in set(self.topics):
            if topic_id == -1:
                continue
            
            topic_indices = [i for i, t in enumerate(self.topics) if t == topic_id]
            if topic_indices:
                topic_docs_embeddings = self.embeddings[topic_indices]
                centroid = np.mean(topic_docs_embeddings, axis=0)
                topic_embeddings[topic_id] = centroid
        
        if len(topic_embeddings) <= 1:
            return {list(topic_embeddings.keys())[0]: {'x': 0, 'y': 0}} if topic_embeddings else {}
        
        topic_ids = list(topic_embeddings.keys())
        centroids_matrix = np.array([topic_embeddings[tid] for tid in topic_ids])
        
        mds = MDS(n_components=2, dissimilarity='euclidean', random_state=42)
        coords_2d = mds.fit_transform(centroids_matrix)
        
        topic_coords = {}
        for i, topic_id in enumerate(topic_ids):
            topic_coords[topic_id] = {
                'x': coords_2d[i, 0],
                'y': coords_2d[i, 1]
            }
        
        return topic_coords
    
    def _calculate_author_contributions(self):
        """Calcule les contributions des auteurs par topic"""
        
        print("👥 Calcul des contributions d'auteurs...")
        
        # Reset des données
        self.author_contributions = {}
        self.author_to_topics = defaultdict(list)
        
        # Compter les contributions par topic
        topic_author_counts = defaultdict(Counter)
        total_processed = 0
        
        for i, topic_id in enumerate(self.topics):
            if topic_id == -1:
                continue
            
            authors = self.metadata[i].get('authors', [])
            total_processed += 1
            
            for author in authors:
                author_clean = author.strip()
                if author_clean and len(author_clean) > 3:
                    topic_author_counts[topic_id][author_clean] += 1
                    self.author_to_topics[author_clean].append({
                        'topic_id': topic_id,
                        'doc_index': i,
                        'title': self.metadata[i].get('title', ''),
                        'year': self.metadata[i].get('year', ''),
                        'hal_id': self.metadata[i].get('hal_id', '')
                    })
        
        # Pour chaque topic, garder les top auteurs
        for topic_id in topic_author_counts:
            top_authors = topic_author_counts[topic_id].most_common(5)
            self.author_contributions[topic_id] = top_authors
            
            # Ajouter aux données du topic
            if topic_id in self.topic_data:
                self.topic_data[topic_id]['top_authors'] = top_authors
        
        print(f"✅ Contributions calculées:")
        print(f"   - {total_processed} documents traités")
        print(f"   - {len(self.author_to_topics)} auteurs uniques")
        print(f"   - {len(self.author_contributions)} topics avec auteurs")
    
    def search_author_topics(self, author_name: str) -> List[Dict]:
        """Recherche les topics auxquels un auteur a contribué"""
        
        # Recherche flexible (case-insensitive, partial match)
        author_name_lower = author_name.lower()
        author_words = author_name_lower.split()
        
        matching_authors = []
        
        # Recherche plus intelligente
        for stored_author in self.author_to_topics.keys():
            stored_author_lower = stored_author.lower()
            stored_words = stored_author_lower.split()
            
            # Vérifier si tous les mots de la recherche sont dans l'auteur stocké
            match_score = 0
            for search_word in author_words:
                for stored_word in stored_words:
                    if (search_word in stored_word or stored_word in search_word) and len(search_word) > 2:
                        match_score += 1
                        break
            
            # Si au moins la moitié des mots matchent
            if match_score >= len(author_words) * 0.6:
                matching_authors.append(stored_author)
        
        if not matching_authors:
            return []
        
        # Combiner les contributions de tous les auteurs correspondants
        topic_contributions = {}
        
        for author in matching_authors:
            author_contribs = self.author_to_topics[author]
            
            for contribution in author_contribs:
                topic_id = contribution['topic_id']
                
                # Compter par topic
                if topic_id not in topic_contributions:
                    topic_contributions[topic_id] = {
                        'count': 0,
                        'documents': [],
                        'topic_data': self.topic_data.get(topic_id, {})
                    }
                
                topic_contributions[topic_id]['count'] += 1
                topic_contributions[topic_id]['documents'].append(contribution)
        
        # Créer la liste finale des topics
        author_topics = []
        for topic_id, data in topic_contributions.items():
            topic_data = self.topic_data.get(topic_id, {})
            author_topics.append({
                'topic_id': topic_id,
                'topic_size': topic_data.get('size', 0),
                'keywords': topic_data.get('keywords_str', ''),
                'contribution_count': data['count'],
                'documents': data['documents']
            })
        
        # Trier par nombre de contributions
        author_topics.sort(key=lambda x: x['contribution_count'], reverse=True)
        
        return author_topics

# Variables globales pour Dash
nlp_processor = AdvancedNLPProcessor()

def create_circles_plot():
    """Crée le graphique des cercles avec hover d'auteurs"""
    
    if not nlp_processor.topic_data:
        fig = go.Figure()
        fig.add_annotation(
            text="Chargement en cours...<br>ou aucun topic trouvé",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False,
            font=dict(size=16, color="orange")
        )
        fig.update_layout(
            title="En attente des données",
            xaxis_title="Composante 1",
            yaxis_title="Composante 2",
            height=600
        )
        return fig
    
    fig = go.Figure()
    colors = px.colors.qualitative.Set3
    
    # Calculer les tailles normalisées
    sizes = [data['size'] for data in nlp_processor.topic_data.values()]
    max_size = max(sizes) if sizes else 1
    
    print(f"🎨 Création des cercles pour {len(nlp_processor.topic_data)} topics")
    
    for i, (topic_id, data) in enumerate(nlp_processor.topic_data.items()):
        normalized_size = max(20, (data['size'] / max_size) * 80 + 30)
        
        # Préparer les infos d'auteurs pour le hover
        top_authors = data.get('top_authors', [])
        if top_authors:
            authors_info = "<br>".join([f"{author} ({count} docs)" for author, count in top_authors[:5]])
        else:
            authors_info = "Aucun auteur trouvé"
        
        hover_text = (
            f"<b>Topic {topic_id}</b><br>"
            f"Taille: {data['size']} documents<br>"
            f"Mots-clés: {data['keywords_str']}<br>"
            f"<br><b>Top Auteurs:</b><br>{authors_info}"
        )
        
        fig.add_trace(go.Scatter(
            x=[data['x']],
            y=[data['y']],
            mode='markers+text',
            marker=dict(
                size=normalized_size,
                color=colors[i % len(colors)],
                opacity=0.7,
                line=dict(width=2, color='black')
            ),
            text=[str(topic_id)],
            textfont=dict(size=14, color='black'),
            name=f'Topic {topic_id}',
            hovertemplate=hover_text + '<extra></extra>',
            customdata=[topic_id]
        ))
    
    fig.update_layout(
        title=f"Topics NLP avec Contributions d'Auteurs ({len(nlp_processor.topic_data)} topics)<br><i>Passez la souris sur un cercle pour voir les top auteurs</i>",
        xaxis_title="Composante 1",
        yaxis_title="Composante 2",
        showlegend=False,
        height=600,
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray')
    )
    
    return fig

def create_keywords_plot(topic_id):
    """Crée le graphique des mots-clés pour un topic"""
    
    if topic_id not in nlp_processor.topic_data:
        return go.Figure()
    
    data = nlp_processor.topic_data[topic_id]
    words = data['words'][:10]
    scores = data['scores'][:10]
    
    words_rev = words[::-1]
    scores_rev = scores[::-1]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=words_rev,
        x=scores_rev,
        orientation='h',
        marker_color='lightblue',
        text=[f'{score:.3f}' for score in scores_rev],
        textposition='outside'
    ))
    
    fig.update_layout(
        title=f"Mots-clés du Topic {topic_id}",
        xaxis_title="Score c-TF-IDF",
        yaxis_title="Mots-clés",
        height=500,
        margin=dict(l=120)
    )
    
    return fig

def create_author_topics_plot(author_topics):
    """Crée un graphique des topics pour un auteur donné"""
    
    if not author_topics:
        fig = go.Figure()
        fig.add_annotation(
            text="Aucun topic trouvé pour cet auteur",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False,
            font=dict(size=14, color="orange")
        )
        return fig
    
    topics = [f"Topic {at['topic_id']}" for at in author_topics]
    contributions = [at['contribution_count'] for at in author_topics]
    keywords = [at['keywords'][:50] + "..." if len(at['keywords']) > 50 else at['keywords'] for at in author_topics]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=topics,
        y=contributions,
        text=keywords,
        textposition='outside',
        marker_color='lightgreen',
        hovertemplate='<b>%{x}</b><br>Contributions: %{y}<br>Mots-clés: %{text}<extra></extra>'
    ))
    
    fig.update_layout(
        title="Topics auxquels l'auteur a contribué",
        xaxis_title="Topics",
        yaxis_title="Nombre de contributions",
        height=400,
        xaxis_tickangle=-45
    )
    
    return fig

# Application Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("🧠 Analyse NLP Avancée - Topics & Auteurs", 
            style={'textAlign': 'center', 'marginBottom': 30, 'color': '#2c3e50'}),
    
    # Panneau de contrôle
    html.Div([
        html.Div([
            html.H3("🔍 Recherche par Auteur"),
            dcc.Input(
                id='author-search',
                type='text',
                placeholder='Tapez le nom d\'un auteur...',
                style={'width': '80%', 'padding': '10px', 'marginRight': '10px'}
            ),
            html.Button('Rechercher', id='search-button', n_clicks=0,
                       style={'padding': '10px', 'backgroundColor': '#3498db', 'color': 'white', 'border': 'none'})
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'}),
        
        html.Div([
            html.H3("📊 Statistiques"),
            html.Div(id='stats-display')
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'})
    ], style={'backgroundColor': '#ecf0f1', 'margin': '20px', 'borderRadius': '10px'}),
    
    # Contenu principal
    html.Div(id='main-content', children=[
        html.Div("Chargement des données...", 
                style={'textAlign': 'center', 'fontSize': 20, 'margin': 50})
    ]),
    
    # Stores
    dcc.Store(id='data-loaded', data=False),
    dcc.Store(id='selected-topic', data=None),
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0, max_intervals=1)
])

@app.callback(
    Output('data-loaded', 'data'),
    Input('interval-component', 'n_intervals')
)
def load_data_callback(n):
    """Charge les données au démarrage"""
    if n > 0:
        # 📝 CHANGEZ LE NOM DE VOTRE FICHIER ICI
        filename = "articles_organised.txt"  
        
        # Vérifier si le fichier existe et donner des suggestions
        import os
        if not os.path.exists(filename):
            print(f"❌ Fichier '{filename}' non trouvé")
            print("💡 Fichiers disponibles dans le dossier:")
            txt_files = [f for f in os.listdir('.') if f.endswith('.txt')]
            for f in txt_files[:5]:  # Montrer les 5 premiers fichiers .txt
                print(f"   - {f}")
            return False
        
        print("=== CHARGEMENT DES DONNÉES NLP ===")
        
        try:
            if nlp_processor.parse_enriched_file(filename):
                if nlp_processor.train_topic_model():
                    return True
                else:
                    print("❌ Échec de l'entraînement du modèle")
                    return False
            else:
                print("❌ Échec du parsing du fichier")
                return False
        except Exception as e:
            print(f"❌ Erreur lors du chargement: {e}")
            import traceback
            traceback.print_exc()
            return False
    return False

@app.callback(
    Output('main-content', 'children'),
    Input('data-loaded', 'data')
)
def update_main_layout(data_loaded):
    """Met à jour le layout principal après chargement"""
    
    if not data_loaded:
        return html.Div([
            html.H3("❌ Erreur lors du chargement des données", style={'color': 'red', 'textAlign': 'center'}),
            html.P("Vérifiez le nom du fichier et le format des données", style={'textAlign': 'center'}),
            html.P("Le fichier doit contenir des articles avec TITRE, AUTEURS, HAL ID, ABSTRACT", style={'textAlign': 'center'})
        ])
    
    if not nlp_processor.topic_data:
        return html.Div([
            html.H3("⚠️ Aucun topic trouvé", style={'color': 'orange', 'textAlign': 'center'}),
            html.P("Le modèle BERTopic n'a pas pu identifier de topics distincts", style={'textAlign': 'center'}),
            html.P("Essayez avec plus de documents ou des textes plus variés", style={'textAlign': 'center'})
        ])
    
    return html.Div([
        # Graphiques principaux
        html.Div([
            html.Div([
                dcc.Graph(
                    id='circles-plot',
                    figure=create_circles_plot(),
                    style={'height': '600px'}
                )
            ], style={'width': '60%', 'display': 'inline-block'}),
            
            html.Div([
                dcc.Graph(
                    id='keywords-plot',
                    figure=create_keywords_plot(list(nlp_processor.topic_data.keys())[0]) if nlp_processor.topic_data else go.Figure(),
                    style={'height': '600px'}
                )
            ], style={'width': '40%', 'display': 'inline-block'})
        ]),
        
        # Panneau de recherche d'auteur
        html.Div([
            html.H3("📈 Analyse par Auteur"),
            html.Div(id='author-analysis'),
            dcc.Graph(id='author-topics-plot', style={'height': '400px'})
        ], style={'margin': '20px', 'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px'}),
        
        # Informations détaillées
        html.Div([
            html.H3("ℹ️ Détails du Topic Sélectionné"),
            html.Div(id='topic-details')
        ], style={'margin': '20px', 'padding': '20px', 'backgroundColor': '#e8f4fd', 'borderRadius': '10px'})
    ])

@app.callback(
    [Output('keywords-plot', 'figure'),
     Output('topic-details', 'children'),
     Output('selected-topic', 'data')],
    [Input('circles-plot', 'clickData')],
    prevent_initial_call=True
)
def update_topic_details(clickData):
    """Met à jour les détails quand on clique sur un topic"""
    
    if clickData is None:
        topic_id = list(nlp_processor.topic_data.keys())[0] if nlp_processor.topic_data else 0
    else:
        topic_id = clickData['points'][0]['customdata']
    
    keywords_fig = create_keywords_plot(topic_id)
    
    # Créer les détails du topic
    if topic_id in nlp_processor.topic_data:
        data = nlp_processor.topic_data[topic_id]
        top_authors = data.get('top_authors', [])
        
        details = html.Div([
            html.H4(f"📊 Topic {topic_id}"),
            html.P(f"📄 Nombre de documents: {data['size']}"),
            html.P(f"🔤 Mots-clés: {data['keywords_str']}"),
            html.P(f"📍 Position: ({data['x']:.2f}, {data['y']:.2f})"),
            html.H5("👥 Top Auteurs:"),
            html.Ul([
                html.Li(f"{author} ({count} documents)")
                for author, count in top_authors
            ])
        ])
    else:
        details = html.P("Sélectionnez un topic en cliquant sur un cercle")
    
    return keywords_fig, details, topic_id

@app.callback(
    [Output('author-analysis', 'children'),
     Output('author-topics-plot', 'figure')],
    [Input('search-button', 'n_clicks')],
    [State('author-search', 'value')],
    prevent_initial_call=True
)
def search_author(n_clicks, author_name):
    """Recherche les topics d'un auteur"""
    
    if not author_name or not author_name.strip():
        return html.P("Tapez le nom d'un auteur et cliquez sur Rechercher"), go.Figure()
    
    author_topics = nlp_processor.search_author_topics(author_name.strip())
    
    if not author_topics:
        analysis = html.Div([
            html.P(f"❌ Aucun résultat pour '{author_name}'"),
            html.P("💡 Essayez avec un nom partiel ou vérifiez l'orthographe")
        ])
        return analysis, go.Figure()
    
    # Calcul du total des contributions
    total_contributions = sum([at['contribution_count'] for at in author_topics])
    total_topics = len(author_topics)
    
    analysis = html.Div([
        html.H4(f"🔍 Résultats pour '{author_name}'"),
        html.Div([
            html.P(f"📊 {total_topics} topics trouvés"),
            html.P(f"📄 {total_contributions} contributions totales"),
            html.P(f"📈 {total_contributions/total_topics:.1f} contributions par topic en moyenne")
        ], style={'backgroundColor': '#e8f4fd', 'padding': '10px', 'borderRadius': '5px', 'margin': '10px 0'}),
        
        html.H5("🎯 Détail par topic:"),
        html.Div([
            html.P([
                html.Strong(f"Topic {at['topic_id']}: "),
                f"{at['contribution_count']} contributions - ",
                html.Em(f"{at['keywords']}")
            ])
            for at in author_topics[:10]
        ])
    ])
    
    topics_fig = create_author_topics_plot(author_topics)
    
    return analysis, topics_fig

@app.callback(
    Output('stats-display', 'children'),
    Input('data-loaded', 'data')
)
def update_stats(data_loaded):
    """Met à jour les statistiques générales"""
    
    if not data_loaded:
        return html.P("Chargement...")
    
    return html.Div([
        html.P(f"📄 Documents: {len(nlp_processor.documents)}"),
        html.P(f"🎯 Topics: {len(nlp_processor.topic_data)}"),
        html.P(f"👥 Auteurs: {len(nlp_processor.authors_set)}")
    ])

def open_browser():
    """Ouvre le navigateur automatiquement"""
    webbrowser.open_new("http://localhost:8050/")

if __name__ == '__main__':
    print("=== LANCEMENT ANALYSE NLP AVANCÉE ===")
    print("🚀 Fonctionnalités:")
    print("   - Support multilingue (FR/EN)")
    print("   - Exclusion automatique des noms d'auteurs")
    print("   - Hover avec top auteurs par topic")
    print("   - Recherche inverse: topics par auteur")
    print("   - Interface interactive complète")
    print("   - Gestion d'erreurs robuste")
    print("\n📝 IMPORTANT: Modifiez le nom du fichier dans le code (ligne ~580)")
    print("🔗 URL: http://localhost:8050/")
    print("\n⏳ Chargement initial peut prendre 1-2 minutes...")
    
    Timer(2.0, open_browser).start()
    app.run(debug=False, use_reloader=False)