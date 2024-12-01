# Othello - Marti Da Silva Ruhoff

Vous trouverez dans **"Marti_Da_Silva_Ruhoff.py"** notre implémentation de alpha-beta pour le jeu othello ainsi que notre fonction d'évaluation.

Notre algorithme s'appuie sur les axes suivants :

- Maximisation du nombre des ses propres pièces stables (qui ne sont plus retournables)
- Minimisation du nombre de pièces stables de l'adversaires
- Maximisation du nombre des ses propres coups légaux (Le nombre de possiblité de coups légaux à disposition)
- Minimisation du nombre de coups possible de l'adversaire

De plus, lors de la descente de l'algorithme alpha-beta, si une victoire est rencontré, le coup qui y amène sera automatiquement jouer, ou inversement dans le cas du joueur inverse.

Notre algorithme alpha-beta n'est pas forcément un enchainement une fois sur deux de min puis de max, mais plutôt de min et de max en fonction de la personne qui joue (notre AI = maximisation, adversaire = minimisation), dans les cas ou un des deux joeurs se voit forcer de passer son tour.
