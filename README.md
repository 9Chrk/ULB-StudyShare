# ULB StudyShare — TUTO vues (Tkinter) + accès base de données

Ce guide explique **concrètement** comment :

1. modifier le layout principal,
2. créer/brancher de nouvelles vues,
3. faire des requêtes vers la base MySQL proprement.

> Le projet suit une logique proche **MVC** :
> - `gui/views/*` = UI pure (widgets Tkinter)
> - `gui/controllers/*` = orchestration des actions utilisateur
> - `core/*` = logique métier + accès DB

---

## 1) Comprendre les fichiers de base (point d’entrée + layout global)

### 1.1 Point d’entrée GUI
- Fichier : `gui/app.py`
- Rôle : créer la fenêtre Tkinter, appliquer la config globale, lancer le contrôleur principal.

Flux actuel :
1. création de `root = tk.Tk()`
2. appel à `configure_root(root)`
3. instanciation de `AppController(root)`
4. `root.mainloop()`

### 1.2 Main layout (fenêtre principale)
- Fichier : `gui/ui_setup.py`
- C’est ici que tu modifies :
  - le **titre de la fenêtre** (`root.title(...)`),
  - la **couleur de fond globale** (`root.configure(bg=...)`),
  - la **taille + centrage** (`_center_window(root, width=..., height=...)`),
  - les **styles globaux ttk** (`ttk.Style()`).

Exemples de modifs fréquentes :

```python
root.title("ULB StudyShare - Dashboard")
_center_window(root, width=1200, height=800)

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 11, "bold"))
```

> ✅ Si tu veux changer le “main layout” (look & feel global), commence toujours par `gui/ui_setup.py`.

---

## 2) Comment le routing entre pages fonctionne

### 2.1 Contrôleur principal
- Fichier : `gui/controller.py`
- `AppController` contient les méthodes de navigation (`show_login`, `show_register`, etc.).

Pour ajouter une nouvelle page (ex: dashboard) :

1. ajouter une méthode dans `AppController`, ex:

```python
def show_dashboard(self):
    self.auth_controller.show_dashboard()
```

2. implémenter la méthode côté contrôleur concerné (ou créer un nouveau contrôleur dédié).

### 2.2 Contrôleur d’auth actuel
- Fichier : `gui/controllers/auth_controller.py`
- Gère la navigation login/register + callbacks boutons.

Bon pattern déjà présent :
- la vue construit les widgets,
- le contrôleur récupère les valeurs des champs,
- le contrôleur appelle `core.auth.service`.

---

## 3) Créer une nouvelle vue Tkinter (pattern recommandé)

### 3.1 Structure d’une vue
Regarde `gui/views/auth/login_view.py` et `register_view.py` :
- une fonction `build(root, callbacks...)`
- appel à `clear_frames(root)` au début
- construction d’un `Frame` principal
- binding des boutons vers des callbacks
- retour optionnel d’un dict des widgets utiles

### 3.2 Exemple: nouvelle vue `dashboard_view.py`

Crée un fichier `gui/views/dashboard_view.py` :

```python
import tkinter as tk
from tkinter import ttk

from gui.ui_helpers import clear_frames


def build(root: tk.Tk, on_load_resumes, on_logout):
    clear_frames(root)

    frame = tk.Frame(root, bg="white")
    frame.place(relx=0.5, rely=0.5, width=700, height=500, anchor="center")

    title = tk.Label(frame, text="Dashboard", font=("Segoe UI", 18, "bold"), bg="white")
    title.pack(pady=20)

    listbox = tk.Listbox(frame, width=80, height=15)
    listbox.pack(pady=10)

    load_btn = ttk.Button(frame, text="Charger mes résumés", command=lambda: on_load_resumes(listbox))
    load_btn.pack(pady=5)

    logout_btn = ttk.Button(frame, text="Logout", command=on_logout)
    logout_btn.pack(pady=5)

    return {"listbox": listbox}
```

---

## 4) Faire des requêtes DB proprement

### 4.1 Outil de connexion existant
- Fichier : `core/db/manager.py`
- `DBManager` est un context manager :

```python
with DBManager() as cursor:
    cursor.execute("SELECT ...", params)
    row = cursor.fetchone()
```

Comportement :
- ouvre une connexion MySQL,
- commit automatique si pas d’exception,
- ferme curseur + connexion à la fin.

### 4.2 Règles à respecter
1. **Toujours paramétrer les requêtes** (`%s`) pour éviter l’injection SQL.
2. Mettre les requêtes dans `core/.../service.py`, pas dans les vues.
3. Garder les vues “bêtes” (UI), la logique dans service + controller.
4. Capturer les erreurs DB côté service (`mysql.connector.Error`) et renvoyer un message propre.

### 4.3 Exemple de service pour dashboard

Créer `core/resume/service.py` :

```python
import mysql.connector
from core.db.manager import DBManager


def list_public_resumes(limit: int = 20):
    try:
        with DBManager() as cursor:
            cursor.execute(
                """
                SELECT r.idResume, r.titre, u.nomUtilisateur, r.datePublication
                FROM Resume r
                JOIN Utilisateur u ON u.idUtilisateur = r.idUtilisateur
                WHERE r.visibilite = 'publique'
                ORDER BY r.datePublication DESC
                LIMIT %s
                """,
                (limit,),
            )
            return True, cursor.fetchall()
    except mysql.connector.Error:
        return False, []
```

### 4.4 Exemple d’appel depuis un contrôleur

Dans un contrôleur GUI :

```python
from core.resume import service as resume_service
import gui.messages as messages


def load_resumes(self, listbox):
    ok, rows = resume_service.list_public_resumes(limit=20)
    listbox.delete(0, "end")

    if not ok:
        messages.show_error(self.root, "Impossible de charger les résumés.")
        return

    for resume_id, titre, auteur, date_pub in rows:
        listbox.insert("end", f"#{resume_id} | {titre} | {auteur} | {date_pub}")
```

---

## 5) Workflow conseillé pour ajouter une nouvelle page

1. **Design UI** : créer `gui/views/<feature>/<page>_view.py` (ou `gui/views/<page>_view.py`).
2. **Callbacks** : exposer dans `build(...)` les callbacks nécessaires.
3. **Controller** : ajouter les méthodes qui récupèrent les inputs et appellent les services.
4. **Service** : ajouter les fonctions SQL dans `core/<feature>/service.py`.
5. **Navigation** : brancher la méthode `show_<page>()` dans `AppController`.
6. **Tests manuels** : lancer l’app et cliquer les parcours utilisateur.

---

## 6) Lancer l’application (rappel)

Selon ton setup, tu peux lancer :

```bash
python main.py
```

ou

```bash
python -m gui.app
```

(si `main.py` route déjà vers `gui.app.run()`, garde `python main.py`).

---

## 7) Checklist rapide “je veux modifier une page principale”

- [ ] Je modifie le style global dans `gui/ui_setup.py`.
- [ ] Je ne mets pas de SQL dans la vue.
- [ ] J’ajoute/édite un service `core/.../service.py` pour parler à la DB.
- [ ] J’appelle ce service depuis un contrôleur.
- [ ] Ma vue reste centrée sur la construction UI + callbacks.
- [ ] Mes requêtes SQL utilisent des placeholders `%s`.

---

## 8) Mapping rapide des fichiers importants

- UI globale : `gui/ui_setup.py`
- Router principal : `gui/controller.py`
- Contrôleur auth : `gui/controllers/auth_controller.py`
- Vues auth :
  - `gui/views/auth/login_view.py`
  - `gui/views/auth/register_view.py`
- DB manager : `core/db/manager.py`
- Services auth + requêtes : `core/auth/service.py`
- Schéma DB : `schema.sql`

---

Si tu veux, je peux aussi te préparer une **version “template prête à copier-coller”** pour une vraie page `home`/`dashboard` complète (vue + controller + service + navigation) directement adaptée à ta structure actuelle.
