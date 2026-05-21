"""Espace de travail post-login avec sidebar + zone de contenu."""

import tkinter as tk

from gui.views.common.sidebar import Sidebar
import gui.views.common.theme as theme


class WorkspaceView(tk.Frame):
    """Vue principale après la connexion.
    - Colonne de gauche : Sidebar avec navigation.
    - Colonne de droite : pile de vues superposées.
    """

    def __init__(self, root: tk.Tk, app_controller, **kwargs):
        self.content_bg = theme.WORKSPACE_BACKGROUND
        super().__init__(master=root, bg=self.content_bg, **kwargs)

        # Initialisation des attributs
        self.root = root
        self.app_controller = app_controller
        self.views = {}

        # Layout global : 2 colonnes (sidebar + contenu)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar à gauche
        self.sidebar = Sidebar(master=self, on_select=self.show_view, active_fg=theme.SIDEBAR_ACTIVE_TEXT, inactive_fg=theme.SIDEBAR_INACTIVE_TEXT)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # Zone de contenu à droite
        self.content_area = tk.Frame(self, bg=self.content_bg)
        self.content_area.grid(row=0, column=1, sticky="nsew")
        self.content_area.grid_rowconfigure(0, weight=1)
        self.content_area.grid_columnconfigure(0, weight=1)

        # Initialiser les vues et la sidebar
        self.create_views()
        self.configure_sidebar_items()
        
        # Ajouter le bouton Exit en bas
        self.sidebar.add_exit_button(on_exit_callback=self.on_exit)

        # Vue par défaut
        self.show_view("dashboard")

    
    # ---------- NAVIGATION ENTRE VUES ----------

    def on_exit(self) -> None:
        """Quitter l'espace de travail et revenir au login."""
        self.destroy()
        self.app_controller.show_login()

    def show_view(self, view_name: str) -> None:
        """Affiche la vue demandée via tkraise sans reconstruire les widgets."""
        frame = self.views.get(view_name)
        if frame is None:
            return

        # Mettre à jour l'état des boutons de la sidebar
        self.sidebar.set_active(view_name)

        # Afficher la vue dans la zone de contenu
        frame.tkraise()


    # ---------- INITIALISATION DES VUES ----------

    def create_views(self) -> None:
        """Instancie toutes les vues de l'application dans la zone de contenu."""
        # Imports locaux pour éviter les imports circulaires
        from gui.views.workspace.dashboard_view   import DashboardView
        from gui.views.workspace.explorer_view    import ExplorerView
        from gui.views.workspace.leaderboard_view import LeaderboardView
        from gui.views.workspace.my_library_view  import MyLibraryView
        from gui.views.workspace.profile_view     import ProfileView
        from gui.views.workspace.shop_view        import ShopView
        from gui.views.workspace.statistics_view  import StatisticsView

        views_config = {
            "dashboard": DashboardView,
            "profile": ProfileView,
            "statistics": StatisticsView,
            "leaderboard": LeaderboardView,
            "shop": ShopView,
            "explorer": ExplorerView,
            "my_library": MyLibraryView,
        }

        for name, ViewClass in views_config.items():
            frame = ViewClass(self.content_area, self.app_controller, bg=self.content_bg)
            frame.grid(row=0, column=0, sticky="nsew")
            self.views[name] = frame

    def configure_sidebar_items(self) -> None:
        """Configure les entrées de navigation de la sidebar."""
        items = {
            "dashboard": "Dashboard",
            "my_library": "My Library",
            "explorer": "Explorer",
            "statistics": "Statistics",
            "leaderboard": "Leaderboard",
            "shop": "Shop",
            "profile": "Profile",
        }
        self.sidebar.set_items(items)
