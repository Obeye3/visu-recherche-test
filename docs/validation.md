# Vérification locale — 11 septembre 2026

Environnement : Windows, Python 3.11, dépendances installées dans un environnement virtuel isolé. Les versions exactes sont consignées dans `requirements/validated-windows-py311.txt`.

Résultat de la suite finale : **47 tests réussis en 15,53 secondes**. Les distributions source et wheel ont été construites avec succès. Les vérifications Ruff et le contrôle des fichiers destinés à Git ne signalent aucune anomalie.

## Contrôles réalisés

- Tests automatisés : filtrage, années, noms accentués, données manquantes, parsing BibTeX, extraction PDF, redirections, jointure du corpus historique, corpus vide, petits corpus, entraînement LDA réel, export HTML, interface Flask et commandes.
- Accès réseau bloqué pendant les tests ; les téléchargements sont simulés.
- Vérification du style et du formatage du code maintenu.
- Vérification des dépendances et construction des distributions Python.
- Contrôle de syntaxe de tous les fichiers Python sélectionnés pour Git, y compris les archives.
- Vérification ciblée des secrets et des exclusions Git.
- Vérification SHA-256 : les 537 fichiers du dossier source sont intacts. 520 fichiers ont été copiés ; seuls le brouillon d’histogramme et le lanceur shell ont été ajustés dans les archives. Les 17 fichiers techniques non recopiés restent dans le dossier source.

## Essais fonctionnels

La démonstration de 12 textes a produit une visualisation à trois sujets. L’interface a été ouverte dans un navigateur, le formulaire soumis et le graphique inspecté. Le bouton de changement de sujet a actualisé la sélection et les mots affichés. Les ressources du graphique sont embarquées dans le HTML.

Une collecte réelle du site S2A a enregistré **887 publications**. Le fichier historique contenait **192 résumés reconnus**, dont **159 associés** aux métadonnées collectées et **33 sans correspondance**. Ces derniers restent dans le fichier initial ; ils n’ont pas été inventés ni associés par approximation de titre.

Une analyse de l’année 2024 sur ce corpus a porté sur **22 résumés**, avec six sujets. **67 publications sélectionnées n’avaient pas de résumé exploitable** et ont été exclues explicitement ; le téléchargement de PDF était désactivé pour cet essai. Le résultat est conservé localement dans `results/s2a-2024.html`.

## Périmètre non validé

Le mode linguistique optionnel et les modèles spaCy n’ont pas été installés. Les expériences BERTopic, graphes, radars et correspondances n’ont pas fait l’objet d’une réexécution complète. La syntaxe correcte des archives ne garantit pas leurs dépendances, leurs chemins ou leurs résultats.

Les exécutions GitHub Actions sous Linux et Python 3.13 ne sont pas encore réalisées : le workflow est prêt, mais aucun dépôt distant n’a été publié. Les essais ne constituent ni une validation scientifique des sujets ni une mesure d’amélioration par rapport aux résultats de 2025.
