# lyon-tour : Serveur

## Description

Le repo est divisé en deux répertoires : ```src/``` et ```env/```.

```src/``` contient les sources de l'application. C'est là qu'on met le code.

```env/``` contient l'environnement de développement. 
C'est ici que le serveur tourne. Normalement il n'y a pas de modifications à faire là

Tout tourne sur 127.0.0.1.

*Explication rapide de différents ports :*
  * 8000 : Serveur de dev/test qui tourne sur directement sur la VM
  * 8081 : Même chose mais quand on lance l'appli avec ```debug``` comme argument
  * 8888 : Serveur sur un container Docker dans la VM. Si ca tourne la, ca tournera sur le serveur distant.
  * 3306 : base de données mysql.


## Prérequis

### Obligatoire 
  * [Vagrant](https://www.vagrantup.com/downloads.html) : permet de lancer une VM avec tout ce qui faut dedans.
  * [VirtualBox](https://www.virtualbox.org/wiki/Download) : nécessaire pour Vagrant.

### Recommandé
  * [PyCharm](https://www.jetbrains.com/pycharm/download/) : IDE pour python.
  * [MySQL Workbench](http://dev.mysql.com/downloads/workbench/#downloads) : GUI pour gérer la BDD

Vous pouvez avoir la version pro avec votre compte INSA : (https://www.jetbrains.com/estore/students/)

## Installation

### Serveur
Une fois Vagrant et Virtualbox installés, clonez ce repo ,
ouvrez un terminal/console, allee dans le dossier ```lyon-tour/env``` et lancez ```vagrant up```.

Le serveur tourne ! 

Vous pouvez aller sur (http://127.0.0.1:8000) ou (http://127.0.0.1:8888).

### PyCharm
 1. Une fois PyCharm intallé, ouvrez le repo depuis PyCharm.
 2. Allez dans ```File > Settings > Project > Project Interpreter```
 3. Cliquez sur la roue pour les réglages
 4. Cliquez sur ```Add remote```
 5. Cliquez Vagrant
 6. Selectionnez le dossier ```env/```
PyCharm est maintenant configuré pour utiliser le python de la VM. (Vous pouvez fermer les réglages)

Pour le moment, si il y a une erreur dans le programme, python crash dans la VM mais ne redémarre pas.
Les logs sont disponibles dans ```env/local/logs/server.log```

Du coup pour relancer l'application on peut utiliser PyCharm : 
  1. En haut à droite, à gauche de la flèche verte, cliquez sur le menu déroulant.
  2. Cliquez sur ```Edit configurations```
  3. Cliquez sur "+", puis "Python"
  4. Mettez le nom que vous voulez en haut
  5. Dans Script mettez ```\app\src\server.py```
  6. Dans Script parameters : ```debug```
  7. Dans Python interpreter, mettez l'interpreteur qu'on a configurer avant.
  8. Cochez en haut : Single Instance Only
 
Vous pouvez maintenant lancer le serveur en cliquant sur la flèche verte et acceder à (http://127.0.0.1:8081)

## Liens utils

  *[Tuto Flask](http://flask.pocoo.org/docs/0.10/quickstart/)
  *[Tuto API Rest](https://flask-restful.readthedocs.org/en/0.3.2/quickstart.html)





