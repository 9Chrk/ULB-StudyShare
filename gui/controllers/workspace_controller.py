"""Contrôleur de l'espace de travail post-login (WorkspaceView + sidebar)."""

from gui.ui_helpers import clear_frames
from gui.views.workspace.workspace_view import WorkspaceView
from gui.ui_helpers import center_window


class WorkspaceController:
    """Instancie et affiche l'espace de travail après connexion."""

    def __init__(self, root, app_controller):
        """Retient la fenêtre racine et le contrôleur principal de l'application."""
        self.root = root
        self.app_controller = app_controller
        self.workspace = None

    def show_workspace(self):
        """Affiche l'espace de travail avec sidebar + contenu."""
        clear_frames(self.root)
        center_window(self.root, width=1280, height=720, resizable=False)
        self.workspace = WorkspaceView(self.root, self.app_controller)
        self.workspace.pack(fill="both", expand=True)
