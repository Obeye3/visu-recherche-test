# Préparer et publier le dépôt

Le dossier `visu-recherche` constitue un seul projet Git. Ne pas publier le dossier parent contenant également la source initiale et l’environnement de test.

## Vérifier la sélection

```bash
git status --short
python scripts/check_repository.py
git add .
git diff --cached --stat
```

Dans la livraison locale, un dépôt Git vide est initialisé sur `main`. Aucun commit ni dépôt distant n’est créé à votre place. Dans une copie provenant de l’archive ZIP, exécuter d’abord `git init -b main`.

Le contrôle vérifie les fichiers que Git sélectionnerait, cherche des motifs de secrets connus, contrôle la syntaxe Python et signale les fichiers de plus de 10 Mo. Il inclut aussi les fichiers déjà suivis : un ajout forcé de données locales est donc détecté.

`data/local/`, `results/`, `docs/reports/local/`, les environnements Python et les sorties de l’application sont ignorés. Les notes historiques sont incluses et restent consultables dans `docs/history/`. Aucun secret réel n’a été identifié par la recherche ciblée initiale ; les chaînes de clé API trouvées dans le prototype LLM sont des exemples `your-api-key-here`.

## Créer le dépôt sur GitHub

Nom proposé : `visu-recherche`.

Description proposée : « Exploration de publications scientifiques : collecte S2A, filtrage de corpus et visualisation de sujets LDA. Projet Artishow, Télécom Paris. »

Sujets proposés : `topic-modeling`, `lda`, `data-visualization`, `nlp`, `flask`, `research`, `python`.

Choisir la visibilité voulue et créer un dépôt vide, sans README ni licence générés automatiquement. Le dépôt local possède déjà sa documentation. La décision de licence reste à prendre avec les auteurs, comme décrit dans `RIGHTS.md`.

Après avoir créé le dépôt, utiliser son URL réelle :

```bash
git add .
git commit -m "Organize research project and add tested LDA application"
git remote add origin https://github.com/VOTRE_COMPTE/visu-recherche.git
git push -u origin main
```

`VOTRE_COMPTE` est un emplacement à remplacer, pas une destination configurée. Après le push, consulter l’onglet Actions pour vérifier les quatre combinaisons système/Python du workflow.

## Archive sans données locales

```bash
python scripts/make_archive.py ../visu-recherche-github.zip
```

L’archive contient la sélection Git du code et de la documentation, sans dossier `.git`. Un fichier existant n’est pas écrasé. Pour une nouvelle exportation, choisir un autre nom ou retirer vous-même l’ancienne archive.
