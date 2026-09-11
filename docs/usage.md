# Utilisation

Les commandes ci-dessous supposent l’environnement virtuel activé. Sous Windows, l’activation est facultative : remplacer `visu-recherche` par `.venv\Scripts\python.exe -m visu_recherche`.

## Démonstration locale

```bash
visu-recherche serve
visu-recherche analyze --topics 3 --output results/demo.html
```

Le premier lance le serveur local ; le second produit un fichier HTML autonome. Les fichiers de sortie existants ne sont pas écrasés : choisir un nouveau nom pour une nouvelle analyse. L’application Web utilise un identifiant distinct pour chaque résultat.

## Charger les publications S2A

```bash
visu-recherche collect --output data/local/publications.json
visu-recherche serve --data data/local/publications.json --download-pdfs
```

La page [Publications S2A](https://s2a.telecom-paris.fr/publications/) est lue une fois par collecte. Les informations sont extraites des notices BibTeX, puis enregistrées dans un JSON. Les doublons d’identifiant sont fusionnés en complétant les champs absents.

L’option `--download-pdfs` autorise l’extraction des résumés manquants pendant une analyse. Elle est désactivée par défaut. Les téléchargements sont limités à quatre simultanément, 25 Mo par document, avec un délai d’inactivité de 30 secondes. Les redirections sont vérifiées ; les hôtes acceptés sont S2A, HAL et arXiv. Un lien vers un autre hébergeur est ignoré avec un message : fournir son résumé dans le JSON pour l’utiliser.

L’interface limite la sélection à 500 publications avant extraction. Réduire le corpus avec les filtres pour obtenir une réponse plus rapide. L’analyse est synchrone ; un second traitement dans le même processus reçoit un message d’attente.

## Réutiliser le corpus fourni avec ce dossier

La copie locale conserve les résumés historiques dans :

```text
data/local/original/pdf_scraping/abstracts_et_hal_v3.txt
```

Pour les joindre aux métadonnées :

```bash
visu-recherche attach-abstracts --data data/local/publications.json --abstracts data/local/original/pdf_scraping/abstracts_et_hal_v3.txt --output data/local/publications-with-abstracts.json
visu-recherche serve --data data/local/publications-with-abstracts.json
```

La jointure compare les identifiants HAL sans suffixe de version (`v1`, `v2`, etc.). Les résumés non associés sont signalés ; deux résumés contradictoires pour le même identifiant déclenchent une erreur. Les résumés existants des publications associées sont remplacés par ceux du fichier explicitement fourni. Le nouveau JSON est distinct du fichier d’entrée.

Dans la livraison locale, `data/local/publications-s2a.json` et `data/local/publications-with-abstracts.json` ont déjà été créés et vérifiés. Vous pouvez lancer directement la deuxième commande `serve` avec ce dernier fichier. Ces corpus ne sont pas inclus dans l’archive GitHub.

## Filtrer et exporter

```bash
visu-recherche analyze --data data/local/publications-with-abstracts.json --year 2024 --topics 6 --output results/s2a-2024.html
visu-recherche analyze --data data/local/publications-with-abstracts.json --author "Gaël Richard" --topics 3 --output results/gael-richard.html
```

Répéter `--year`, `--author` ou `--keyword` pour sélectionner plusieurs valeurs. Les valeurs d’un filtre sont réunies par OU ; les filtres distincts par ET. Un mot-clé correspond à une expression entière, pas à une sous-chaîne. Casse, accents, espaces et apostrophes sont normalisés pour la comparaison ; l’affichage garde les noms du corpus.

`--permanent-only` applique la liste historique de 22 membres présente dans le prototype de 2025. Cette liste n’est pas présentée comme l’effectif actuel de S2A. Sans cette option, l’application conserve tous les auteurs.

## Format JSON

```json
{
  "identifiant-de-mon-document": {
    "title": "Titre du document",
    "authors": ["Prénom Nom"],
    "keywords": ["audio source separation"],
    "year": "2024",
    "type": "Journal Articles",
    "pdf_link": null,
    "abstract": "Le résumé complet du document, avec au moins huit mots exploitables."
  }
}
```

Les listes `authors` et `keywords` peuvent être vides ; l’année peut être absente. L’identifiant n’a pas besoin d’être un identifiant HAL pour analyser un corpus personnel. Un minimum de deux résumés est nécessaire ; le nombre de sujets ne peut dépasser leur nombre. L’extraction PDF est heuristique : elle recherche une section Abstract ou Résumé dans les trois premières pages, s’arrête avant Introduction ou Keywords, et n’effectue pas d’OCR.

## Mode linguistique facultatif

```bash
python -m pip install -e ".[nlp]"
python -m spacy download en_core_web_sm
python -m spacy download fr_core_news_sm
visu-recherche serve --linguistic
```

Ce mode ajoute la détection de langue et la lemmatisation. Aucun modèle n’est téléchargé automatiquement au lancement. Les modèles spaCy et leurs téléchargements n’ont pas été validés dans la vérification locale initiale. Voir les différences avec le prototype dans [architecture.md](architecture.md).

## Emplacement des résultats et du serveur

```bash
visu-recherche serve --port 5050 --work-dir results/session
```

Les résultats Web sont stockés dans `.visu-recherche/visualizations/` par défaut. Pour importer l’application avec Flask :

```bash
python -m flask --app "visu_recherche.web:create_app" run
```

`VISU_RECHERCHE_DATA` permet de choisir le JSON et `VISU_RECHERCHE_HOME` le dossier de résultats dans ce mode. Le serveur fourni est destiné à un usage local sur `127.0.0.1`. Une installation publique multi-utilisateur nécessite une architecture de déploiement, une authentification et une file de calcul adaptées.
