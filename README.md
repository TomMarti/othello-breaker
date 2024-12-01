# Othello - Marti Da Silva Ruhoff

Vous trouverez dans **"ShadyStrategist"** notre implémentation de alpha-beta pour le jeu othello ainsi que notre fonction d'évaluation.

Notre algorythme explore et favorise les coups suivant:
- Ceux qui augmentent le nombre de pièce qui sont capturé de manière définitive.
- Les coups qui augmentent notre nombre de possible coup dans le futur (ce qui en contre partie va favoriser un long temps de réflexion)
- Et vice versa (on va chercher à minimiser ces deux variables pour l'adversaire)