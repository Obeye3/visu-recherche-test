# Réorganisation du dossier fourni

Source : `visu-recherche-main-recent/visu-recherche-main`. La préparation est une copie organisée ; le dossier fourni reste intact.

L’inventaire initial comprend **537 fichiers, 483 382 571 octets**, dont 90 fichiers `.py`, deux scripts Python sans extension, un script shell et 273 PDF. Aucun dépôt `.git`, fichier de dépendances ou licence n’était présent. Le README était vide.

## Destination des fichiers

| Contenu initial | Destination | Nombre |
| --- | --- | ---: |
| Scripts Python et shell | `experiments/original/` | 93 |
| Textes, PDF d’articles et données | `data/local/original/` | 313 |
| Images, visualisations HTML, graphes Gephi/GEXF | `results/legacy/` | 101 |
| Notes et documents Markdown | `docs/history/` | 10 |
| Présentation, rapport et explication du NMF | `docs/reports/local/` | 3 |
| Caches, paramètres d’éditeur et fichiers vides de structure | Non recopiés | 17 |

Le [manifeste](migration-manifest.csv) indique le chemin initial, la destination, la catégorie, la taille et l’empreinte SHA-256 de chaque fichier initial. Les données et résultats restent locaux grâce au `.gitignore`. Les ressources du modèle de formulaire historique sont dans les résultats archivés ; elles ne sont pas utilisées par la nouvelle application.

Deux scripts Python sans extension ont reçu `.py`. Les autres noms historiques ont été conservés pour faciliter leur rapprochement avec le suivi du projet. Le paquet maintenu emploie des noms importables, sans espaces ni accents.

## Corrections du parcours principal

| Défaut constaté | Comportement de la nouvelle application |
| --- | --- |
| Formulaire `years` mais filtre `year` | Clé `years` prise en charge, adaptateur pour `year` |
| Années entières ou chaînes incohérentes | Comparaison uniforme sur quatre chiffres |
| Accents, doubles espaces et apostrophes différents | Normalisation commune des critères et des métadonnées |
| Filtre implicite par permanents même sans sélection | Option explicite, liste historique identifiée comme telle |
| Variables `year` et titre lues avant initialisation | Champs facultatifs validés après analyse de la notice BibTeX |
| PDF parfois récupéré dans une autre notice | Recherche limitée à la publication courante |
| TLS désactivé, absence de limites de téléchargement | TLS actif, taille bornée, délais et redirections contrôlées |
| Messages d’échec ajoutés comme résumés | Échecs exclus du modèle et consignés séparément |
| Jusqu’à 50–70 téléchargements simultanés | Quatre par défaut, huit au maximum dans la fonction |
| Fichiers PDF temporaires jamais supprimés | Lecture en mémoire |
| Traitement Flask sous `if __name__ == "__main__"` | Application importable via une fabrique `create_app` |
| Sortie unique dans un dossier `static` absent | Dossiers créés au besoin et identifiant unique par résultat |
| Modèles lourds chargés à l’import | Chargement au moment du calcul ; mode linguistique optionnel |
| Corpus vide ou nombre de sujets incompatible | Messages explicites avant entraînement |
| Suppression totale du vocabulaire sur petits corpus | Seuils adaptés, textes vides exclus sans décaler les identifiants |
| Graphique dépendant de ressources externes | Export HTML embarquant JavaScript et CSS |

La nouvelle implémentation est sous `src/`. Les anciens scripts restent une référence : elle ne les modifie pas tous pour leur donner artificiellement le statut d’application vérifiée.

## Ajustements des archives

La fonction vide de `histogramme_distribution.py` produisait une erreur de syntaxe. Elle signale désormais explicitement qu’elle n’était pas implémentée. Le lanceur shell `lancer_bertopic.sh` est neutralisé : il ne lance plus l’installation Homebrew ni les changements de profil shell. Le corps historique reste consultable après la sortie anticipée.

Deux doublons exacts ont été identifiés et conservés pour la traçabilité : `citation_commune.py` / `citation_commune_vf.py`, et deux brouillons vides `filee_choix_auteurs.py` / `visualisation_choix_keyword.py`. Les archives peuvent encore contenir des chemins locaux ou des dépendances anciennes ; leur statut est expliqué dans `experiments/README.md`.

## Préparation GitHub

Ajout d’un README, guides d’usage et d’architecture, fichier de dépendances, configuration de formatage, tests, vérification des fichiers et workflow CI. L’attribution du travail collectif a été conservée. Aucune licence n’a été choisie à la place des auteurs. Aucun dépôt distant n’a été créé ni alimenté.
