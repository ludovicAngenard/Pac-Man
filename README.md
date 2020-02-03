# Ma version de Pac-Man 

## Contexte

Voici un code fini en Python que j'ai réalisé seul pendant mon temps libre lors de mon début de première année en bachelor informatique.

----------------------------------------------------------------------------------------------------------------------------------------
## Qu'est ce que c'est? 

Mon jeu reprend les règles classiques du pac man avec quelques ajouts sympatiques comme des déguisements débloquables en augmentant de niveaux et en achetant avec de la monnaie virtuelle que vous pouvez gagner au cours d'une partie. Bien sur vous incarnez un petit camembert jaune au départ qui doit manger le plus de billes jaunes possible. Quatre fantômes de couleurs  qui se déplacent aléatoirement vont essayer de vous manger, alors faites attention. A partir du niveau 10, vous débloquerez une difficulté supplémentaire, je vous laisse la découvrir.

----------------------------------------------------------------------------------------------------------------------------------------
## Installation 

Pour installer le Pac-man, vous devez juste télécharger python 3.0 au minimum. Aussi, vous devez télécharger ces bibliothèques: 

* pickle 
* tkinter 
* time 
* pygame 
* random

```
  from tkinter import *
  from tkinter import messagebox
  from random import *
  import pickle
  import time
  import pygame
```
Vous pouvez tout simplement télécharger édupython en cliquant sur ce lien : https://edupython.tuxfamily.org/ qui est un éditeur où toutes les bibliothèques sont déjà préinstallé et où vous pouvez éxécuter le code en appuyant sur le triangle vert au niveau de la barre d'outil. Une fois ceci fait, **vous devez juste éxécuter le script dans le fichier "run.py"**

----------------------------------------------------------------------------------------------------------------------------------------
## Comment jouer ?

Pour commencer une partie, vous devez cliquer sur le bouton commencer tou simplement. Une fois cliqué, la partie se lance directement avec une musique. Utilisez les flèches directionnelles pour déplacer votre personnage. Une fois que vous avez mangé toutes les billes jaunes, déplacez vous une nouvelle fois et la partie s'arrête et vous retournez au menu de départ. Lors de la partie, toutes les 200 billes jaunes mangées, une pièce apparait, prenez là pour pouvoir acheter des déguisements par la suite. Dès que vous vous faîtes manger par un fantôme, vous gardez quand même votre score.

----------------------------------------------------------------------------------------------------------------------------------------
## Les déguisements et bonus

Une fois dans le menu cliquez sur le bouton "déguisement". Selon votre niveau, vous allez tomber sur deux étagères plus ou moins vide. La première étagères contient tous les déguisements et la seconde contient la difficulté débloquable a partir du niveau 10. A chaque niveau supplémentaire, vous débloquez un nouveau déguisement. Cependant, vous ne l'avez pas encore dans votre collection car il va falloir l'acheter avec votre monnaie virtuelle en cliquant sur le déguisement en question. Si vous n'avez pas assez de monnaie, rien ne se produira. En revanche, si vous en avez assez, une boîte de messages vous demande si vous voulez vraiment l'acheter puis si vous voulez l'activer. Pour changer de déguisements, vous avez juste a cliquer sur un déguisement déjà acheté pour l'activer.

----------------------------------------------------------------------------------------------------------------------------------------
## Sauvegarde

Si vous avez fait un bon score et que vous avez des déguisements ou que vous avez débloqué la difficulté maximum au niveau 10. Mais que vous ne voulez pas tout perdre, vous pouvez être rassuré car tout est sauvegardé une fois que vous avez fini une partie ou acheté un déguisement. Si vous voulez réinitialiser votre partie, lancez le code dans les fichiers "récompenses.py" puis "progression.py". 

----------------------------------------------------------------------------------------------------------------------------------------
## Les fichiers

### Voici la liste des fichiers python :

* run.py
* progression.py
* récompenses.py

### Voici la liste des fichiers où sont stockées vos données:

* donnes
* récompenses

### Voici la liste des fichiers sons: 

* bubul.wav
* bruitperdu.wav
* clap.wav
* bipargent.wav
* Kubbi-Ember-04Cascade.wav ( Titre:  Cascade Auteur: Kubbi Source: http://www.kubbimusic.com/ Licence: https://creativecommons.org/licenses/by-sa/3.0/deed.fr  Téléchargement (8MB): https://auboutdufil.com/?id=485 )
* apparition.wav
