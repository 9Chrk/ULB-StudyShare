"""Espace de travail post-login avec sidebar + zone de contenu."""

import tkinter as tk

from gui.views.common.sidebar import Sidebar


class WorkspaceView(tk.Frame):
    """Vue principale après la connexion.
    - Colonne de gauche : Sidebar avec navigation.
    - Colonne de droite : pile de vues superposées.
    """

    def __init__(self, root: tk.Tk, app_controller, **kwargs):
        super().__init__(master=root, bg="#1a1a2e", **kwargs)

        self.root = root
        self.app_controller = app_controller
        self._views = {}

        # Layout global : 2 colonnes (sidebar fixe + contenu)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar à gauche
        self.sidebar = Sidebar(
            master=self,
            on_select=self.show_view,
            bg="#141429",
            active_fg="#1DE9B6",
            inactive_fg="white",
        )
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # Zone de contenu à droite
        self.content_area = tk.Frame(self, bg="#1a1a2e")
        self.content_area.grid(row=0, column=1, sticky="nsew")
        self.content_area.grid_rowconfigure(0, weight=1)
        self.content_area.grid_columnconfigure(0, weight=1)

        # Initialiser les vues et la sidebar
        self._create_views()
        self._configure_sidebar_items()

        # Vue par défaut
        self.show_view("dashboard")

    # ---------- INITIALISATION DES VUES ----------

    def _create_views(self) -> None:
        """Instancie toutes les vues de l'application dans la zone de contenu."""
        # Imports locaux pour éviter les imports circulaires
        from gui.views.dashboard_view import DashboardView
        from gui.views.profile_view import ProfileView

        views_config = {
            "dashboard": DashboardView,
            "profile": ProfileView,
            # "shop": ShopView,
            # "leaderboard": LeaderboardView,
        }

        for name, ViewClass in views_config.items():
            frame = ViewClass(self.content_area, self.app_controller, bg="#1a1a2e")
            frame.grid(row=0, column=0, sticky="nsew")
            self._views[name] = frame

    def _configure_sidebar_items(self) -> None:
        """Configure les entrées de navigation de la sidebar."""
        items = {
            "dashboard": "Dashboard",
            "profile": "Profil",
            # "shop": "Boutique",
            # "leaderboard": "Leaderboard",
        }
        self.sidebar.set_items(items)

    # ---------- NAVIGATION ENTRE VUES ----------

    def show_view(self, view_name: str) -> None:
        """Affiche la vue demandée via tkraise sans reconstruire les widgets."""
        frame = self._views.get(view_name)
        if frame is None:
            return

        # Mettre à jour l'état des boutons de la sidebar
        self.sidebar.set_active(view_name)

        # Afficher la vue dans la zone de contenu
        frame.tkraise()
