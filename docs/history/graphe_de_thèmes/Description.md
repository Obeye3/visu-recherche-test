Le graphe des thèmes est un graphe où chaque sommet est un mot (thème) et les arêtes représentent les liens entre eux. Plus le poids est grand (ou plus il y a d'arêtes), plus le lien est fort.

Etapes: 

1. Pré-traitement:

Nettoyer le corpus (supprimer la ponctuation, convertir en minuscules, enlever les mots vide (stop words), tokeniser le texte: séparer les mots)

2. Extraction des thèmes/mots-clés:

On utilise des techniques de traitement automatique de langage, dans notre cas c'est le TF-IDF (regarder https://www.youtube.com/watch?v=C3V2Lf1Y9Qk&ab_channel=KNIMETV)
(Apparemment, le TF-IDF s'applique sur un seul document)
Il y a aussi une autre technique: LDA (Latent Dirichlet Allocation)

3. Calcul de la similarité
4. Construction du graphe
5. Visualisation
