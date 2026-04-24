# ULB-StudyShare - Guide de continuation


## 1. Objectif

Le projet est deja structuré.

Ce qu'il reste a faire:

1. Ecrire les requetes SQL dans core/repository.
2. Faire les services metier dans core/services.
3. Exposer les donnees par vue via gui/controller.py.
4. Afficher les donnees dans les vues gui/views/workspace.


## 2. Workflow à suivre

Flux de donnees:
Vue -> AppController -> Service -> Repository -> DB

Concretement:

1. Ajouter une fonction SQL dans un fichier repository.
2. Ajouter une fonction metier dans un service.
3. Ajouter une methode agregée dans AppController pour la vue cible.
4. La vue appelle une seule methode AppController et affiche le resultat.

Important:

1. Pas de SQL dans les vues.
2. Pas de logique UI dans repository/services.
3. Requetes toujours parametrees avec %s.


## 3. Exemple concret appliqué (Dashboard + username)

Ce pattern est deja implemente.

Etape 1 - Repository:
core/repository/user_repository.py
(renvoie le résultat d'une commande SQL)

- get_user_info(cursor, user_id) -> Optional[UserInfo]
- Retourne une dataclass UserInfo (pas un dict brut !!)

Etape 2 - Service:
core/services/user_service.py
(Crée une connexion à la DB avec DBManager et le transmet à une méthode dans repository)

- get_current_username(user_id) -> str
- Retourne le usersame présent dans la DB

Etape 3 - AppController:
gui/controller.py

- get_dashboard_data() -> dict
- Centralise les donnees necessaires au Dashboard

Etape 4 - Vue:
gui/views/workspace/dashboard_view.py

- data = self.app_controller.get_dashboard_data()
- Affichage avec data['username']


## 4. Convention pour les prochaines vues

Pour chaque vue Workspace (Explorer, Statistics, etc.):

1. Ajouter les requetes dans un repository dedie (ex: core/repository/explorer_repository.py).
2. Ajouter la logique metier dans un service dedie (ex: core/services/explorer_service.py).
3. Ajouter une methode agregée dans AppController (ex: get_explorer_data()).
4. Dans la vue, faire un seul appel AppController puis render.


## 5. Typage et robustesse

1. Environnement actuel: python3 est en 3.9.
2. Eviter la syntaxe de type X | None (non compatible 3.9).
3. Utiliser Optional[...] et Tuple[...] depuis typing.
4. Preferer des dataclasses (ex: UserInfo) aux dicts quand possible.


## 6. Lancement du projet

1. Copier .env_example en .env.
2. Completer les valeurs de connexion MySQL dans .env.
3. Installer les dependances:
   pip install -r requirements.txt
4. Lancer:
   python3 main.py



## 7. TODO par vue Workspace

### Dashboard (dashboard_view.py)

Objectif: vue d'accueil avec resume rapide du compte et de l'activite.

TODO:

1. Afficher le nom utilisateur connecte (deja fait).
2. Afficher points actuels, niveau, titre actif.
3. Afficher un mini resume des dernieres actions (ex: dernieres publications, dernieres evaluations).

### Profile (profile_view.py)

Objectif: consultation du profil utilisateur.

TODO:

1. Afficher les infos profil: username, email, date inscription.
2. Afficher points, niveau, titre actif.
3. Afficher les objets actifs (badge/titre/theme) si presents.

### Explorer (explorer_view.py)

Objectif: gestion des cours et consultation de resumes.

TODO:

1. Afficher la liste des cours.
2. Permettre de filtrer/rechercher un cours.
3. Afficher les resumes associes au cours selectionne.
4. Ajouter l'action de publication d'un resume associe a un cours.
5. Ajouter l'ajout d'un nouveau cours si autorise.
6. Ajouter l'action d'evaluation d'un resume (note/commentaire).

### My Library (my_library_view.py)

Objectif: gestion des resumes de l'utilisateur connecte.

TODO:

1. Afficher la liste des resumes publies par l'utilisateur.
2. Permettre modification de ses propres resumes.
3. Permettre suppression de ses propres resumes.
4. Afficher les evaluations recues sur ses resumes.

### Statistics (statistics_view.py)

Objectif: visualiser les requetes analytiques demandees dans l'enonce.

TODO (obligatoire):

1. Top 10 utilisateurs ayant le plus de points.
2. Utilisateurs ayant publie dans au moins 3 cours differents.
3. Cours ayant le plus de resumes publies.
4. Resumes les mieux notes (moyenne max) pour chaque cours.
5. Utilisateurs n'ayant jamais publie de resume.
6. Objet cosmetique le plus achete.
7. Utilisateurs ayant depense plus de points qu'ils n'en ont disponibles.
8. Nombre moyen de resumes publies par utilisateur.

### Leaderboard (leaderboard_view.py)

Objectif: classement des utilisateurs selon leurs points.

TODO:

1. Afficher un classement ordonne par points decroissants.
2. Afficher au minimum: rang, username, points, niveau.
3. Ajouter une mise en evidence de l'utilisateur courant.

### Shop (shop_view.py)

Objectif: boutique cosmetique et gestion des activations.

TODO:

1. Afficher le catalogue d'objets cosmetiques.
2. Permettre l'achat d'objets via points.
3. Afficher les objets deja possedes par l'utilisateur.
4. Permettre l'activation d'un badge.
5. Permettre l'activation d'un titre.
6. Optionnel selon schema: activation du theme profil.

### Rappel implementation par vue

Requetes SQL dans core/repository/`<vue>`_repository.py.

Logique metier dans core/services/`<vue>`_service.py.

Methode agregée dans gui/controller.py: get_`<vue>`_data().

Affichage dans la vue via un seul appel AppController.


Bon dev.


## 8. Maquette : EXEMPLE DE VUE!!

![1775420038966](assets/guide/1775420038966.png)

![1775420051583](assets/guide/1775420051583.png)

![1775420136996](assets/guide/1775420136996.png)

![1775420148157](assets/guide/1775420148157.png)

![1775420156629](assets/guide/1775420156629.png)

![1775420162571](assets/guide/1775420162571.png)
