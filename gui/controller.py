"""Contrôleur principal de l'application."""

from tkinter import font, ttk

from gui.controllers.auth_controller import AuthController
from gui.controllers.workspace_controller import WorkspaceController


class AppController:
    """Contrôle la navigation entre les écrans."""
    
    def __init__(self, root):
        self.root = root

        # instances des contrôleurs
        self.auth_controller = AuthController(root, self)
        self.workspace_controller = WorkspaceController(root, self)
        
        # point d'entrée de l'application
        self.show_login()
        
        
    # ---------- FONCTIONS DE NAVIGATION ENTRE VUES ---------
    
    def show_login(self):
        """Affiche l'écran de connexion."""
        self.auth_controller.show_login()
    
    def show_register(self):
        """Affiche l'écran d'inscription."""
        self.auth_controller.show_register()
        
    def show_workspace(self):
        """Affiche l'espace de travail après une connexion réussie."""
        self.workspace_controller.show_workspace()
