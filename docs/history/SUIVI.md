# SUIVI

## Periode 3

### 14/02   (Séance 1)

Documentation et test de quelques techniques de visualisation:

- Obeye: recherche sur les graphes de thèmes et application sur python (utilisation de numpy, networkx, matplotlib, scikit-learn, NLTK). (Voir dossier graphe_de_thèmes)
- Mohamed : Recherches sur le prétraitement des données en particulier la gestion des doublons par clustering puis prise de décision dans chaque cluster , dépot d'un code qui effectue un prétraitement basic des données d'in site . 
-   Lina : 
TH1 Documentation à partir de la bibliographie suivante KeywordScape: Visual Document Exploration using Contextualized Keyword Embeddings. Dans un premier temps j'ai utilisé la bibliothèque allenai-science parse disponible en open source sur Github pour le traitement de texte que j'ai cloné et stocké dans le dossier keyword_scape. j'ai installé java, et sdb nécéssaire pour la compilation du projet disponible dans le répértoire Github suivant : https://github.com/allenai/science-parse .
 TH2 : Je me rends compte en essayant de compiler le projet que celui-ci n'est plus maintenu, il dépend de plusieurs bibliothèques qui ne sont plus disponibles sur les dépôts de Maven et Bintray.


- Rayane : recherche sur les Nuage de mots et application sur python (utilisation de numpy, networkx, matplotlib, Beautifulsoup). (Voir dossier WordCloud)


### 18/02   (Séance 2)

- Réunion avec l’encadrant

- Rédaction du planning en groupe 

- Répartition des tâches : 2 sous-groupes de 2, groupe A (Linha et Obeye) chargé du Web scrapping et groupe B (Mohamed et Rayane) chargé du pre-processing

- Organisation du Git

Lina : Dans le cadre de l'organisation du git , Ajout d'un dossier pipelines_finalisés en plus d'un fichier versions.md qui associe chaque version à une visualisation et son domaine d'application . Ajout d'un code de web scrapping.



### 04/03   (Séance 3)

- Consultation des références bibliographiques (A Survey of Visual Analytics Techniques
 for Machine Learning ; KeywordScape: Visual Document Exploration using Contextualized
 Keyword Embeddings)

Groupe A:
 - Obeye: ajout de résumés de ces références sur "NOTES.md" ; documentation sur html et Beautifulsoup ; Code de scraping en utilisant "requests" et Beautifulsoup de bs4 ; test sur différentes pages
  Il reste à voir le crawling si nécessaire.

Groupe B:
- Mohamed : code de tokenization avec les exressions regulières et dépot d'une explication de leur construction (les exp regulières)
- Rayane  : Code d'obtention du vocabulaire a partir des tokens et code de la conversion fichier.txt en string

### Hors Séance :

- Lina : élaboration d'un code de webscrapping pour les fichiers Wikipédia et test sur la page Wikipédia Chaton,
amélioration du code pour supprimer tout les éléments indésirables html

### 11/03   (Séance 4)

  Réunion de groupe en début de séance : présentation et explication de ce que chaque groupe a fait (~20 minutes)

- Rayane : Code de détection de langue et inclusion du code de supprimer_stopwords.py dans pipeline_1.py. 
Débuggage du code résultant et test de la pipeline_1 sur un article du site S2A avec une visualisation en nuage de mots.
- Lina : 1TH -> Réunion , 2TH : web scrapping du site S2A : extraction du nom de chaque thèses, membres et l'URL du site pdf.
- Obeye : Nouveau code de web scraping en qui intègre des fonctions de filtrage dans le code de Linha. Résolution de problème d'affichage et d'extraction: trop de sauts de ligne et des espaces supprimés.
Autres tests sur les pages wikipédia: le code marche très bien sur ceux-ci.
Inspection du site S2A pour adapter le code.
- mohamd :Rassemblement du code en une première pipeline (sans visualisation), puis application pour visualisation par rectangles de tailles proportionnelles à leurs occurences. 


### 18/03   (Séance 5)

- [TH1] (Rayane) : Ajout de la pipeline pour la visualisation par nuage de mots. 
- [TH2] (Rayane) : Ajout d'un paramètre du nombre minimal d'occurence pour rendre le vocabulaire plus exhaustif.

- Mohamed : Depot du code du treemap avec amelioration du pretraitement (normalisation et supression des prépositions)

- [TH1] (Lina) : intégration dans le fichier pipeline_1.py du code Webscrapping1.1+ Changement du code Webscrapping pour éliminer les symboles latex du style frac, display...
- [TH2] (Lina) : Modification du code de webscrapping du site s2a pour l'extraction de toutes les thèses (953) + Ecriture du résultat dans le fichier s2a_theses.txt

- Obeye: Test de scraping sur la page de publications de S2A (on arrive à extraire les titres, auteurs et liens). Essai d'extraction des fichiers pdf: avec pdfplumber extraction réussie mais avec un problème d'espaces, avec PyMuPDF (ou fitz) pas encore réussie.

### 25/03   (Séance 6)

- [TH2] (Rayane) : Ajout d'un code de prétraitement pour récuperer les dates SUBMITTED et LAST REVISED.

- Obeye : Code de scraping de pdf en utilisant PyMuPDF, soit à partir d'un pdf téléchargé soit à partir d'un lien. Documentation sur le graphe de force comme autre méthode de visualisation et sur le topic modeling.
- Mohamed : Depot de code pour créer des coreespandances (auteurs - publications) , utilisation de LDA pour créer un graphe de thème.
- Lina : Intégration du code d'extraction de thèses pdf depuis un site web dans le code du web scrapping. ( Echec du test )
### 01/04   (Séance 7)

- [TH1] (Rayane) : Recherche sur la méthode de Topic Model par Non-negative Matrix Factorization (NMF) .
- [TH2] (Rayane) : Rédaction d'une documentation expliquant son principe et certaines subtilités.

- Obeye : Documentation sur la LDA plus spécifiquement pour pouvoir faire d'autres méthodes de visualisations et les comparer. Ajout d'un document explicatif et essai d'application de la LDA sur les 17 thèses les plus récentes à l'aide de Python et des outils de scikit-learn. Il reste des erreurs de codes à régler.

- [TH1 & TH2] (Lina)Correction des erreurs dans s2a_scrapping_with_pdfs + un premier résultat pour les 50 premières thèses avec pdf inclus

### 08/04   (Séance 8)

Groupe A :

- [TH1] (Lina) : Documentation du principe générale de topic modelling (sources dans le MD) et de la technique LDA.
- [TH2] (Lina) : Ajout de la documentation sur le principe mathématique sous-jacent pour le LDA ( vecteurs de probabilités Dirichlet) + Ajout d'une première 
version de code qui utilise LDA de Gensim et qui l'applique au fichier s2a_these_with_pdfs.txt
- Obeye : [TH1] Plus de documentation sur la LSA: fonctionnement, avantages, inconvénients et coherence score. 
[TH2] Ajout d'un code python qui marche cette fois et essai sur le fichier texte s2a_these_with_pdfs.

Groupe B :

- [TH1] (Rayane) : Documentation rapide du principe du Topic Modeling et rédaction d'une documentation courte de la technique BERTopic (clustering).
- [TH2] (Rayane) : Première visualisation avec la librairie BERTopic puis rédaction d'une première version d'un code fonctionnelle de la technique BERTopic sans cette librairie.
[TH1] (Mohamed) : Documentation de la décomposition NMF et code de vectorisation du texte. 
[TH2] (Mohamed) : Visualisation des topics du site S2A en utilisant La décomposition NMF , évaluation de la pertinence en fonction du nombre de topics

### 15/04   (Séance 9)

- Obeye: [TH1 & TH2] Révision du travail fait jusque-là: scraping page web et pdf, visualisations, LSA topic modeling et analyse du résultat de la LSA.
  Travail sur la présentation PPT pour la présentation intermédiaire.
- Rayane: [TH1 & TH2] Révision du travail fait jusque-là: tokenisation, visualisations, BERtopic modeling et analyse des résultats.
  Travail sur la présentation PPT pour la présentation intermédiaire.
- Lina :[TH1 & TH2] Révision du travail fait jusque-là: création de l'outline de la présentation, visualisations, LDA topic modeling et analyse des résultats.
  Travail sur la présentation PPT pour la présentation intermédiaire.
  -Mohamed :[TH1 &2] Description de l'avancement sur la présentation pour ka présentation intérmédiaire
  
### 16/04   (Séance 10)

- Lina : [TH1] : visualisation du graphe de niveau de cohérence en fonction du nombre de topic choisis LDA + visualisation interactive du résultat du LDA
sur les 59 thèses de s2a publications.
- Mohamed : Determination  du nombre optimal de topics pour NMF et avancement dans la présentation
- Obeye : Application de la LSA sur le nouveau document texte avec plus de thèses, coherence score et nombre de thèmes optimal.

### 17/04 (Hors-séances)

14h-->15h : Réunion avec l'encadrant pour la présentation intermédiaire.

## Periode 4

### 05/05   (Séance 11)
(Nous nous sommes mis d'accord avec l'encadrant de continuer de travailler sur deux méthodes de topic-modeling: Bertopic et LDA)
Réunion pour faire un récapitulatif de la dernière réunion avec l'encadrant.

- Rayane & Mohamed : récupération des prénoms/noms des auteurs dans le fichier s2a_thèses.txt.

- Obeye : [TH1] Documentation sur LDA et Bertopic, compréhension de la visualisation de LDA

Réunion avec l'encadrant avant [TH2]

Nouvelle répartition des tâches: 
Groupe A (Lina et Mohamed) : Tableau de contingence (topics en utilisant LDA), histogrammes, analyse en correspondance
Groupe B (Rayane et Obeye) : Bertopic, clustering hiérarchique, implémentation de distance et densité

- Obeye: [TH2] essai de modification du web scraping pour résoudre le probème d'extraction des auteurs, discussion avec Rayane sur le clustering hiérarchique et les tâches à faire.
- Lina : [TH1] Ajout du code de visualisation intéractive pour LDA & l'output en html pour un nombre de topic 12.
- Lina : [TH2] modification du code de s2a_scrapping de tel sorte à structurer les données extraites + Ajout de l'output (fichier txt) résultant de l'application du code
sur le site de S2A
- Lina : [HORS TH] Rédaction d'un layout du rapport environnementale.
- Lina : [HORS TH] Ajout de prétraitement de texte plus optimale pour mieux extraire le nom des membres sans texte parasite ( métadonnées qui ne nous
intéressent pas) dans le code de s2a_scrapping.py + nouvel output S2a_thèses_1.txt

### Hors séance : 

- Obeye et Rayane: code de clustering hiérarchique ascendant avec figure pour visualiser le nombre de clusters.


### 12/05   (Séance 12)
 - Lina : [TH1]  Nouveau code LDA (lda_table_de_contingence_histogrammes.py ) appliqué aux données extraites ( regExp ) de s2a_thèses_1.txt pour faire une table de contingence et visualiser les histogrammes topic / membres et membres / topic
 - Lina : [TH2] Modification de lda_table_de_contingence_histogrammes pour visualiser les histogrammes de façon plus claire et pertinente. Visualisation en barres empilés.

 - Obeye : Essai du code de BERTopic, beaucoup de problèmes comme la version de la bibliothèque umap, débogage, tests et vérifications à la main avec Rayane des output (clusters) pour des choix de distances différentes (cosine ou euclidean), participation à la rédaction du rapport sur les enjeux sociaux et environnementaux.

 - Rayane : Implémentation et débuggage de du code de clustering hiérarchique, recherche de la meilleur méthode de distance avec Obeye.
### Hors séance : 

- Tous : Préparation de la présentation pour l'audit de groupe.
- Tous : Rédaction du rapport sur les enjeux environnementaux, sociaux et légaux de notre projet.

### 19/05   (Séance 13)

- Tous : Audits de groupe.

### Hors séance :

- Tous : Rendez-vous avec l'encadrant le 22/05 pour faire le point sur l'avancement du projet et sur l'organisation pour les semaines à venir.
- Rayane : Début de rédaction d'une documentation sur la bibliothèque fournie par l'encadrant.

### 26/05   (Séance 14)
  - Rayane : [TH1] Rédaction de la documentation . 
  - Rayane : [TH2] Ajout d'un paramètre de comparaison entre modèles à la pipeline Bertopic : le diversity score.
  - Lina : [TH1] Ajout d'un code qui extrait depuis le fichier s2a_members.txt les domaines de prédilections des membres : il se nomme extracting_members_labels_from_txt_file
  - Lina : [TH1] Code d'étiquetage autonome utilisant scibert & les domaines de spécialisations des membres permanents du site de s2a comme topics potentiels
  - Lina : [TH2] Code d'étiquetage autonome utilisant uniquement LDA et le poids de chaque mot pour assigner une étiquette à un topic en se basant uniquement sur un dictionnaire de dictionnaires hiérarchisés comme suit : Domaines, puis sous-domaines. Il se base surtout sur la distribution de probabilité de chaque domaine potentiel dans le topic.
  - Lina : [TH2] Ajout aussi d'un dictionnaire_labels.py qui contient les dictionnaires des domaines & sous-domaines pertinents
  - Obeye : [TH1] Résolution des problèmes avec les bibliothèques: utilisation de conda, analyse des résultats de score de diversité pour différents nombres de mots-clés
  [TH2] Premier code de visualisation pour BerTopic

  -Mohamed : [Th1] Mise en place du nouveau scraping  pour selectionner uniquement les articles des profs permanants 
  [TH2]: Adaptation de la pipeline de LDA et analyse en correspandance pour le nouveau scrapping.

### Hors séance

- Rayane : Test d'un deuxième paramètre de comparaison entre modèles à la pipeline Bertopic : l'inverted rbo score.

- Obeye : Application de bertopic_clustering_hier_asc sur les articles, deuxieme essai de visualisation de bertopic.
-Mohamed: Finalisation de la pipeline + Création de diagrammes radars pour un choix intéractif.
### 02/06   (Séance 15)

- Lina [TH1&TH2] : Implémentation d'un algorithme d'étiquetage améliorée
-Mohamed [TH1&TH2] : Résolution des problèmes d'etiquettage (plusieurs topics avec meme etquette), et l'absence de quelques auteurs de la visualisation.


### Hors séance

- Rayane : Première implémentation d'un algorithme de génération de graphes dont les articles sont les nodes et il y a un edge si il y a un mots-clés en commun entre deux articles.

- Lina : Création d'un code qui retourne un dictionnaire type { hal_ids : titre, keywords, authors } pour tous les articles disponibles dans le site de S2A. (Dictionnaire_halids_keywords.py)
- Implémentation d'une pipeline d'étiquetage qui se base sur les keywords de chaque articles et les titre en utisant les n-grammes pour obtenir des thèmes concrets associés à chaque topic et applications aux articles permanents ( etiquetage_articles_permanents.py)

- Obeye : Création d'une première version du poster et révision du code de visualisation.
-Mohamed : Création de dictionnaire {hal ids : titres , auteurs , keywords}  et  exploitation de cette dérnière pour ajouter un aspect intéractif et ajoutant une partie de filtrage en amont du modèle LDA.
### 23/06   (Séance 16)
- Lina [TH1&TH2] : Construction d'une pipeline automatisé  dans le dossier pipelines finalisés : pipeline interactive.
Cette pipeline consiste en : 
- Load_data un fichier python qui fait le scrapping de tous le site de S2A et stocke les métadonnées dans un dictionnaire de dictionnaire indexé par les hal_ids
de la forme { "hal_id:293743" : {"title : , "keywords" : , "authors" : , type : , "year" : , "pdf_url"}}
- filter_parameters : un fichier qui permet de filtrer les éléments du dictionnaire qu'on veut en fonction des paramètres : keywords, authors, year et type
- extract_pdf : un fichier qui prend en entrée le dictionnaire filtrer et qui stocke l'abstract des articles choisis dans un documents
- config : un fichier qui rassemble toutes les étapes précédentes dans une fonction prepare_corpus qui renvoie le documents du corpus prêt à être donnée en entrée
à un algorithme de topic modeling.

- Lina [TH3] : Adaptation de tous les codes de topic modeling pour les insérer dans la pipeline interactive dont LDA & Bert_Topic
- Lina [TH4] : Analyse de la table de contingence keywords, topic pour mettre en exergue les sous-thèmes contenus dans chaque topic 

- Tous [TH4] : Rendez-vous avec l'encadrant pour présenter l'avancement et avoir des retours.
- Rayane [TH1&TH2]: Implémentation d'un algorithme de génération de graphes de co-citations  (dont les articles sont les nodes et il y a un edge si il y a une citation en commune)
- Rayane [TH3&TH4]: Implémentation d'un algorithme de génération d'un graphe de citations
- Obeye : Filtrage et traitement du fichier "articles_permanents" en utilisant python pour enlever le contenu (cleaned_2) ou le contenu et l'abstract (cleaned_1)
(pas de schémas donc pour une vingtaine d'articles cela a été fait manuellement). Retest de la visualisation BerTopic sur ceci avec une section en bas pour ajouter plus d'informations.
Les mots clés sont filtrés sauf qu'il reste de les séparer des noms des auteurs.


-Mohamed: Création d'interface web (front et back end) pour unne visualisation intéractive , et visualisations des entropies des auteurs grace au modèle LDA.
### 24/06   (Séance 17)
Tous : réunion avec l'encadrant.
- Lina  [TH1&TH2] : Finalisation de la pipeline et application à BerTopic & LDA. Viusalition des topics spécifique à chaque fois à un seul auteur permanent : Ceci, d'abord en lançant BerTopic qui détermine un nombre de topic optimal, puis LDA avec ce même nombre de Topic. Cette visualisation offrait une comparaison entre les deux modèles.
- Lina [TH3&TH4] : Correction des irrégularités dans l'extraction des abstracts des pdf ( dans le fichier extract_pdf.py dans pipeline interactive) et normalisation du format pour chaque article + Mise en place d'un fallBack pour l'extraction du lien pdf contenant les articles ( dans le fichier load_data() dans pipeline interactive)
-Mohamed:[TH1 TH2] Débuggage l'ANC .
-Mohamed:[TH3 TH4] Début de création d'interface web pour l'ANC .
- Obeye : meilleure version plus organisée du fichier texte (articles_organised) avec toutes les informations importantes, et fichier avec hal_id et abstracts, avec codes. Amélioration de la visualisation BERTopic pour inclure top auteurs, la recherche par auteur donnant les topics auxquels ils ont contribué et le nombre des contributions. Pour le fichier texte, il faut ajouter d'autres articles, et la visualisation a des bugs.
### 25/06   (Séance 18)
- Lina[TH1&TH2] : Création d'une interface Web contenant un boîtier de paramètres : menu déroulant permettant de choisir les mots-clés voulus, auteurs, et années
de publication via Flask. Adapter le Backend pour affichier la visualisation de LDA et appeler le programme de topic modeling, en tout la validation des paramètres, utilise presque tout les fichiers de la pipeline dont load_data, filter_data, config & lda_visualisation.
-Lina[TH3] : Amélioration du preprocessing pour LDA : Lemmatisation et introduction des bigrams & trirgams
-Lina[TH4] : Tests et analyse quant à la bonne valeur de threshold & min_count pour l'appirition de bigrames pertinents dans les top mots clés d'un topic dans la visualisation LDA (modifs amenés à lda_visualisation)
- Mohamed : [TH1 TH2] Construction d'une innterface web pour la visualisation par graphes.
- Mohamed[TH3 TH4] Rassemblement de toute les visuamisations dans une mem interface.
]
- Rayane[TH1&TH2] : Ajout d'une légende et mise en évidence des auteurs permanents sur le graphe
- Rayane[TH3&TH4] : Ajout de paramètres pour l'interactivité
- Obeye : Correction du code de visu. BERTopic et essais de nouveau scraping pour inclure tous les articles avec les abstracts (impossible avec python pour quelques uns donc extraction manuelle). Première version de visualisation LDA pour la comparaison avec BERTopic.

### 26/06   (Séance 19)

- Tous : réunion avec l'encadrant.
-Mohamed : Réglage de la séléctivité des keywords dans le filtrage + finalisation de l'inrerface de controle.
- Obeye : Dernières modifications et corrections des codes de visualisation LDA et BERTopic, essai sur un corpus plus riche.

### 27/06   (Séance Finale)