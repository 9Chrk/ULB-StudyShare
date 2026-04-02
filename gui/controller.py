"""Contrôleur principal de l'application."""

from tkinter import font, ttk

from gui.controllers.auth_controller import AuthController
from gui.controllers.dashboard_controller import DashboardController


class AppController:
    """Contrôle la navigation entre les écrans."""
    
    def __init__(self, root):
        self.root = root

        # instances des contrôleurs
        self.auth_controller = AuthController(root, self)
        self.dashboard_controller = DashboardController(root, self)
        
        # point d'entrée de l'application
        self.show_login()
        
        
    # ---------- FONCTIONS DE NAVIGATION ENTRE VUES ---------
    
    def show_login(self):
        """Affiche l'écran de connexion."""
        self.auth_controller.show_login()
    
    def show_register(self):
        """Affiche l'écran d'inscription."""
        self.auth_controller.show_register()
        
    def show_dashboard(self):
        """Affiche le tableau de bord après une connexion réussie."""
        self.dashboard_controller.show_dashboard()