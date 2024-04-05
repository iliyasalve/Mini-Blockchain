# Mini-Blockchain

## Description du projet

**Une application qui implémente les principales fonctions de Blockchain.**

Principales fonctionnalités de l'application :

* _Exploitation minière de pièces ;_

* _Effectuer des transactions entre utilisateurs ;_

* _Affichage du réseau blockchain complet stocké par l'utilisateur dans le noeud ;_

* _Vérifier si le réseau Blockchain est valide (personne n'a tenté de compromettre une transaction) ;_

* _Ajout d'autres nœuds à la liste de l'utilisateur pour les futures transactions entre nœuds ;_

* _Résoudre les conflits dans les données stockées par différents nœuds afin de stocker la même version du réseau Blockchain ;_

* _Consulter les pièces de coins d'un utilisateur._

## Comment démarrer un projet

Pour réussir le lancement d'un projet, vous devez suivre les étapes suivantes dans l'ordre :

1. Lancer le noeud

Pour démarrer un nœud, utilisez la console et entrez une commande au format suivant :

_python noeud.py filename port_

où,

- port : numéro de port, par exemple 80

- filename: le nom du fichier où seront stockées les clés privées et publiques

_Remarque : si vous le souhaitez, vous pouvez exécuter plusieurs nœuds à l'aide de plusieurs consoles._

2. Lancez l'application
Pour exécuter l'application, utilisez la console et entrez une commande au format suivant :

_application python.py_

> [!TIP]
> Le côté serveur de l'application est écrit à l'aide de la bibliothèque [Flask](https://pypi.org/project/Flask/).

> [!IMPORTANT]
> Toutes les bibliothèques nécessaires qui nécessitent une installation sont stockées dans le fichier requirements.txt

> [!NOTE]
> Ce code s'est exécuté et a fonctionné correctement sous Windows 10 et Python version 3.12.1

> [!WARNING]
> Ce projet a été créé pour se familiariser avec les principes de fonctionnement du réseau Blockchain et son utilisation pour des projets réels est fortement déconseillée.

---------------

**An application that implements the main functions of Blockchain.**

Main features of the application:

* _Coin Mining;_

* _Making transactions between users;_

* _Showing the complete blockchain network stored by the user in the node;_

* _Checking whether the Blockchain network is valid (no one tried to compromise any transaction);_

* _Adding other nodes to the user's list for future transactions between nodes;_

* _Resolving conflicts in data stored by different nodes in order to store the same version of the Blockchain network;_

* _Viewing a user's coins._

> [!TIP]
> The server side of the application is written using the [Flask](https://pypi.org/project/Flask/) library.

> [!IMPORTANT]
> All necessary libraries that require installation are stored in the requirements.txt file.

> [!NOTE]
> This code ran and worked correctly on Windows 10 and Python version 3.12.1

> [!WARNING]
> This project was created to get acquainted with the principles of operation of the Blockchain network and it is highly not recommended for use for real projects.
