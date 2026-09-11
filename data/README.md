# Données locales

`local/original/` contient les corpus texte, tableaux et PDF du dossier fourni. Ce répertoire est ignoré par Git ; un clone neuf ne contient donc aucun article téléchargé.

Le fichier `src/visu_recherche/data/demo.json` est le seul corpus livré dans le paquet installable. Il est synthétique et clairement identifié comme tel.

Les commandes `collect` et `attach-abstracts` permettent de créer un corpus JSON dans `local/`. Voir le guide d’utilisation. Les nouvelles sorties ne remplacent pas un fichier existant.
