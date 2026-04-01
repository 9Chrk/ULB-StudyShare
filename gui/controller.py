"""Contrôleur de l'authentification GUI."""

from tkinter import font, ttk

from gui.controllers.auth_controller import AuthController


class AppController:
    def __init__(self, root):
        self.root = root

        # instances des contrôleurs
        self.auth_controller = AuthController(root, self)
        
        # point d'entrée de l'application
        self.show_login()
        
        
    # ---------- FONCTIONS DE NAVIGATION ENTRE VUES ---------
    
    def show_login(self):
        self.auth_controller.show_login()
    
    def show_register(self):
        self.auth_controller.show_register()
