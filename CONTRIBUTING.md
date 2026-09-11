# Contribuer

Installer le projet avec l’option `dev`, puis exécuter les tests et les vérifications indiqués dans le README.

Le code utilisé par l’application appartient à `src/visu_recherche/`. Un nouveau module ne doit ni télécharger de données ni lancer un modèle au moment où il est importé. Les accès réseau sont explicites et les tests utilisent des réponses simulées.

Lorsqu’un changement modifie la sélection du corpus, le prétraitement ou les paramètres du modèle, préciser son effet scientifique dans la documentation. Ajouter un test qui illustre le défaut corrigé ou le nouveau comportement.

Les recherches de `experiments/original/` constituent des références historiques. Pour promouvoir une expérience, isoler son entrée/sortie dans le paquet, documenter ses dépendances et vérifier son résultat sur un corpus contrôlé.

Ne pas ajouter les environnements Python, données locales ou sorties de calcul à Git. Utiliser `python scripts/check_repository.py` pour inspecter la sélection avant publication.
