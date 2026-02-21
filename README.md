MAPMAKER 

Ce projet est une application Python permettant de créer des cartes de tuiles interactives. Il implémente des algorithmes de résolution de contraintes pour garantir la cohérence géographique (rivières, reliefs, types de terrains).

## Installation et Lancement

1. **Installer les dépendances** :
   ```bash
   make install
   ```
2. **Lancer le programme** :
   ```bash
   make run
   ```
3. **Lancer les tests unitaires** :
   ```bash
   make test
   ```
   
## Commandes d'utilisation

Une fois l'application lancée, vous pouvez interagir avec la carte de la manière suivante :

* **Souris (Clic Gauche)** : Cliquez sur une case vide pour voir les tuiles compatibles et choisir celle à placer.
* **Touches Directionnelles** : Explorez la carte. Le monde s'étend dynamiquement et sauvegarde les zones que vous quittez.
* **Touche 'C' (Compléter)** : Remplir automatiquement les cases vides de la zone visible.
* **Touche 'S' (Sauvegarder)** : Enregistre votre création dans un fichier JSON pour la reprendre plus tard.
