# lyon-tour : Serveur

## Description

Le repo est divisé en deux répertoires : ```src/``` et ```env/```.

```src/``` contient les sources de l'application. C'est là qu'on met le code.

```env/``` contient l'environnement de développement. 
C'est ici que le serveur tourne. Normalement il n'y a pas de modifications à faire là

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

Du coup pour relancer l'application on peut utiliser PyCharm.





