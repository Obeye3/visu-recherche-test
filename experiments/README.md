# Recherches historiques

Ce dossier conserve les scripts du projet Artishow de 2025. Le point d’entrée maintenu est l’application `visu_recherche`, décrite dans le README principal. Les archives ne sont ni installées dans le paquet Python, ni importées par les tests de l’application.

| Dossier dans `original/` | Sujet |
| --- | --- |
| `web_scraping/`, `pdf_scraping/` | Collecte et extraction de textes |
| `prétraitement_données/` | Tokenisation, nettoyage et comptage |
| `topic modeling/` | LDA, BERTopic, NMF, LSA, radars et correspondances |
| `Etiquetage_LDA/` | Étiquetage des sujets |
| `graphe_article/` | Graphes d’auteurs, de sujets et de citations |
| `graphe_de_thèmes/` | Graphes de thèmes, correspondances et essais LLM |
| `Pipelines_finalisés/` | Étapes d’intégration, dont la chaîne LDA ayant servi à la nouvelle application |
| `interfaces_controle/` | Prototypes de contrôle Web et analyses de correspondances |

Les scripts BERTopic ne constituent pas une commande unifiée : ils utilisent selon les versions `sentence-transformers`, `umap-learn`, `hdbscan`, `bertopic`, `dash`, `plotly` et parfois `octis`. Choisir un script précis et un environnement séparé pour reprendre ces expériences. Le lanceur shell historique a été désactivé car il installait Homebrew et modifiait un profil utilisateur.

Les données ont été rangées dans `data/local/original/` et les sorties dans `results/legacy/`, en gardant leur chemin d’origine sous ces racines. Les anciens scripts peuvent nécessiter une adaptation de leurs chemins pour les lire. Ils peuvent également exécuter des traitements dès l’import et référencer des bibliothèques absentes ; une vérification syntaxique ne valide pas leur exécution ni leurs conclusions scientifiques.

Les deux scripts originellement sans extension ont été nommés `analys_coreespondances.py` et `interfaces_controle.py`. Le brouillon `histogramme_distribution.py` signale explicitement son absence d’implémentation.

Pour retrouver la destination d’un fichier initial, consulter [`docs/migration-manifest.csv`](../docs/migration-manifest.csv). Les versions exactes reçues restent aussi dans le dossier source conservé à côté de la livraison.
