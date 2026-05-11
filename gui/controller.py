"""Contrôleur principal de l'application."""

from tkinter import font, ttk

from gui.transitions import with_alpha_transition
from gui.controllers.auth_controller import AuthController
from gui.controllers.workspace_controller import WorkspaceController
from core.services import user_service


class AppController:
    """Contrôle la navigation entre les écrans."""
    
    def __init__(self, root):
        self.root = root
        
        # utilisateur connecté
        self.current_user_id = None

        # instances des contrôleurs
        self.auth_controller = AuthController(root, self)
        self.workspace_controller = WorkspaceController(root, self)
        
        # point d'entrée de l'application
        with_alpha_transition(self.root, self.show_login)
        
        
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
        
        
    # ---------- FONCTIONS DE RÉCUPÉRATION DE DONNÉES ----------
    
    """
    Ces fonctions sont appelées par les vues pour obtenir les données à afficher.
    Elles font le lien entre les vues et les services métier.
    """
    
    def get_dashboard_data(self) -> dict:
        return {
            "user_id": self.current_user_id,
            "username": user_service.get_current_username(self.current_user_id),
        }
        
    def get_explorer_data(self) -> dict:
        return {
            
        }

    def get_leaderboard_data(self) -> dict:
        from core.services import leaderboard_service
        return {
            "username": user_service.get_current_username(self.current_user_id),
            "leaderboard": leaderboard_service.get_leaderboard(),
        }
        
    def get_my_library_data(self) -> dict:
        return {
            
        }
        
    def get_profile_data(self) -> dict:
        return {
            
        }
        
    def get_shop_data(self) -> dict:
        return {
            
        }
    
    def get_statistics_data(self) -> dict:
        return {
            
        }
    
