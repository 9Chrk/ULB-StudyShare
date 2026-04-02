"""Contrôleur de l'espace de travail post-login (WorkspaceView + sidebar)."""

from gui.ui_helpers import clear_frames
from gui.views.workspace_view import WorkspaceView


class WorkspaceController:
    """Instancie et affiche l'espace de travail après connexion."""

    def __init__(self, root, app_controller):
        self.root = root
        self.app_controller = app_controller
        self._workspace = None

    def show_workspace(self):
        """Affiche l'espace de travail avec sidebar + contenu."""
        # On nettoie les anciennes frames (login) une seule fois
        clear_frames(self.root)

        # Crée et affiche la vue principale de workspace
        self._workspace = WorkspaceView(self.root, self.app_controller)
        self._workspace.pack(fill="both", expand=True)
