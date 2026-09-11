# Visu Recherche

Explorer les thèmes d’un ensemble de publications scientifiques : collecter les métadonnées S2A, sélectionner un corpus, extraire ses résumés et visualiser les sujets obtenus avec LDA.

Projet issu du travail collectif **Artishow, Télécom Paris (2025)**. Cette version organise les recherches et propose une application LDA installable. Les expériences BERTopic, graphes de citations, analyses de correspondances et nuages de mots restent consultables dans [`experiments/`](experiments/README.md).

## Démarrer

Python **3.11 recommandé**. Dans le dossier du projet, sous Windows :

```powershell
py -3.11 -m venv .venv
.venv\Scripts\python.exe -m pip install -e ".[dev]"
.venv\Scripts\python.exe -m visu_recherche serve
```

Sous Linux ou macOS :

```bash
python3.11 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/python -m visu_recherche serve
```

Ouvrir **[http://127.0.0.1:5000](http://127.0.0.1:5000)**, puis cliquer sur **Analyser les publications**. La démonstration contient 12 textes synthétiques et des auteurs fictifs. Une fois les dépendances installées, elle fonctionne hors connexion, y compris le graphique interactif.

## Ce qui fonctionne dans cette version

- Application Flask : filtres par auteur, mot-clé et année ; choix du nombre de sujets ; liste des publications par sujet dominant.
- Collecte des métadonnées BibTeX depuis le site S2A et import des résumés du corpus historique.
- Extraction PDF facultative, avec délais d’attente, téléchargements limités et bilan des documents ignorés.
- LDA avec Gensim, graine aléatoire fixée ; export pyLDAvis en HTML autonome.
- Tests de non-régression, vérifications de style et workflow GitHub Actions.

Les méthodes expérimentales conservées dans `experiments/` ne sont pas intégrées à la nouvelle interface. Le mode linguistique spaCy est facultatif et nécessite des modèles supplémentaires. Voir les [limites scientifiques](docs/architecture.md#méthode-et-limites).

## Utiliser de vraies publications

Après activation de l’environnement, la commande `visu-recherche` est disponible. Sans activation, remplacer cette commande par `.venv\Scripts\python.exe -m visu_recherche` sous Windows.

```bash
visu-recherche collect --output data/local/publications.json
visu-recherche serve --data data/local/publications.json --download-pdfs
```

La collecte enregistre uniquement les métadonnées. Dans l’interface, sélectionner un auteur ou une année avant d’analyser un corpus important. Les résumés déjà fournis sont utilisés en priorité ; seuls les manquants peuvent déclencher un téléchargement. Le [guide d’utilisation](docs/usage.md) décrit le format JSON et la réutilisation des données livrées.

Pour exporter la démonstration directement :

```bash
visu-recherche analyze --topics 3 --output results/demo.html
```

## Organisation

```text
visu-recherche/
├── src/visu_recherche/     Application, collecte, traitement et modèle LDA
├── tests/                 Tests automatisés, sans accès réseau
├── docs/                  Guides, migration et notes de recherche
│   ├── history/           Documents de travail historiques
│   └── reports/local/     Rapports et présentation conservés localement
├── experiments/original/  Scripts de recherche de 2025, classés par dossier d’origine
├── data/local/            Corpus et PDF, ignorés par Git
├── results/               Figures et exports HTML, ignorés par Git
├── scripts/              Vérification du contenu destiné à GitHub
└── .github/workflows/     Vérifications à chaque push et pull request
```

Les dossiers locaux sont créés au besoin et ne sont pas présents dans un clone neuf. Le [registre de migration](docs/migration-manifest.csv) permet de retrouver chacun des 537 fichiers fournis. Le [bilan des changements](docs/migration.md) détaille les corrections et le statut des travaux historiques.

## Développement

```bash
python -m pytest
python -m ruff check src tests scripts
python -m ruff format --check src tests scripts
python -m build
python scripts/check_repository.py
```

Les résultats de la vérification locale sont consignés dans [`docs/validation.md`](docs/validation.md). Le workflow teste Python 3.11 et 3.13 sous Linux et Windows ; ses exécutions GitHub commenceront après publication.

## Équipe et diffusion

Les notes du projet attribuent le travail initial à **Lina, Mohamed, Obeye et Rayane**. Les contributions restent décrites dans le [suivi historique](docs/history/SUIVI.md).

Aucune licence de code n’accompagnait le dossier fourni. Cette préparation n’attribue pas de licence à la place des auteurs. Les publications PDF, corpus extraits et rapports sont conservés localement et exclus de Git. Voir [`RIGHTS.md`](RIGHTS.md) et le [guide GitHub](docs/github.md) avant de choisir les éléments à diffuser.
