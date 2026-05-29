"""Contrôleur responsable de la logique d'authentification côté GUI."""

from core.services import auth_service
from gui.transitions import with_alpha_transition
import gui.messages as messages
import gui.views.auth.login_view as login_view
import gui.views.auth.register_view as register_view


class AuthController:
    """Gère la navigation et les actions entre les vues login/register."""

    def __init__(self, root, app_controller):
        """Conserve les dépendances nécessaires aux vues d'authentification."""
        self.root = root
        self.app_controller = app_controller

    def show_login(self):
        """Affiche la vue de connexion."""
        # On reconstruit la vue pour repartir d'un état propre après chaque navigation.
        login_view.build(
            root=self.root,
            on_login=self.login,
            on_register_link=self.app_controller.show_register,
        )

    def show_register(self):
        """Affiche la vue de création de compte."""
        # Même principe pour l'inscription: la vue est recréée à chaque affichage.
        register_view.build(
            root=self.root,
            on_register=self.register,
            on_login_link=self.app_controller.show_login,
        )

    # --------------------------------------------------------
    # Méthodes de gestion de l'authentification
    # --------------------------------------------------------

    def login(self, user_entry, password_entry):
        """Tente de connecter l'utilisateur à partir des champs de saisie."""
        username = user_entry.get()
        password = password_entry.get()

        # On efface immédiatement le mot de passe pour éviter qu'il reste affiché.
        password_entry.delete(0, "end")
        is_ok, message, user_id = auth_service.check(username, password)

        if is_ok:
            user_entry.delete(0, "end")
            self.app_controller.current_user_id = user_id
            with_alpha_transition(self.root, self.app_controller.show_workspace)
        else:
            messages.show_error(self.root, message)

    def register(self, user_entry, password_entry, confirm_password_entry, email_entry):
        """Tente de créer un compte à partir des champs d'inscription."""
        username = user_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        # Les champs sensibles sont effacés dès la lecture pour limiter l'exposition.
        password_entry.delete(0, "end")
        confirm_password_entry.delete(0, "end")

        if password != confirm_password:
            messages.show_error(self.root, "Les mots de passe ne correspondent pas.")
            return

        is_ok, message = auth_service.add(username, password, email)

        if is_ok:
            user_entry.delete(0, "end")
            email_entry.delete(0, "end")
            messages.show_info(self.root, "Inscription réussie.")
            self.show_login()
        else:
            messages.show_error(self.root, message)
