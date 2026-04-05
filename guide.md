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

## 7. Definition of done

1. Les donnees affichees dans les vues viennent de la DB.
2. SQL rangé dans core/repository uniquement.
3. Les services portent la logique metier.
4. Chaque vue utilise une methode agregée AppController.
5. L'application reste lancable.

Bon dev.
