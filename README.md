# Jeu de Cartes Pygame

Bienvenue dans le jeu de cartes Pygame ! Ce jeu est basé sur les le jeu de cartes de bataille, où deux joueurs s'affrontent pour gagner des manches. Ici, pas de second joueur mais l'ordinateur comme adverssaire. Le jeu a été retravailler pour que le jeu ne dure pas indéfiniment. Il y a 3 manches ou chaque joueurs possède un nombres de cartes entre chaque manche. Le joueur qui remporte le plus de manches gagne la partie. 

**Voici comment vous pouvez lancer le jeu :**

## Prérequis

Avant de lancer le jeu, assurez-vous d'avoir installé Python et Pygame sur votre ordinateur.

- Python : Vous pouvez télécharger Python depuis le site officiel [python.org](https://www.python.org/downloads/).

- Pygame : Vous pouvez installer Pygame en exécutant la commande suivante dans votre terminal ou invite de commande :

(Vous pouvez aussi lancer ce projet depuis Thonny/EduPython)

## Lancement du Jeu

### Option 1 : Lancement à partir du code source (main.py)

1. Ouvrez un terminal ou une invite de commande.

2. Naviguez vers le répertoire où vous avez enregistré les fichiers du jeu.

3. Exécutez la commande suivante pour lancer le jeu : 

```python main.py```

Le jeu devrait se lancer et s'afficher dans une fenêtre Pygame.

### Option 2 : Lancement à partir du fichier exécutable (.exe)

1. Allez dans le dossier /dist

2. Double-cliquez sur le fichier main.exe.

Le jeu devrait se lancer et s'afficher dans une fenêtre Pygame avec le terminal de debug.

## Comment Jouer

rêgles du jeu :
 - on divise le paquet en trois tas égaux
 - on prends le premier tas et on distribue aux deux joueurs
 - une par une, on retourne les cartes en même temps, le joueur qui a la carte la plus élevée gagne les cartes
 - le joueur qui à le plus de nombre de carte à la fin de la manche remporte un point
 - on recommence avec la deuxième manche
 - en cas d'égualité à la fin des deux manches on recommence avec la troisième manche
 le gagnant est celui qui a remporté le plus de manches parmi les 3 manches

Vous devrez appuyer sur espace pour passer chaque tour.
