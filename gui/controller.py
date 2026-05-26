"""Contrôleur principal de l'application."""

from gui.transitions import with_alpha_transition
from gui.controllers.auth_controller import AuthController
from gui.controllers.workspace_controller import WorkspaceController
from core.models.shop import ActivationResult
from core.models.shop import PurchaseResult
from core.models.shop import ShopData
from core.models.leaderboard import LeaderboardData
from core.models.statistics import StatisticsData
from core.models.user import DashboardData
from core.models.user import ProfileData
from core.services import user_service
from core.services import shop_service
from core.services import statistics_service
from core.services.my_library_service import LibraryService
from core.services.explorer_service import ExplorerService


class AppController:
    """Contrôle la navigation entre les écrans."""

    def __init__(self, root):
        """Conserve la fenêtre racine et instancie les contrôleurs spécialisés."""
        self.root = root


        self.explorer_service = ExplorerService()

        # utilisateur connecté
        self.current_user_id = None

        # instances des contrôleurs
        self.auth_controller = AuthController(root, self)
        self.workspace_controller = WorkspaceController(root, self)
        self.library_service = LibraryService()

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

    def get_dashboard_data(self) -> DashboardData:
        """Retourne les données nécessaires au tableau de bord."""
        return user_service.get_dashboard_info(self.current_user_id)

    def get_explorer_data(self) -> dict:
        """Retourne les données de l'explorateur, encore non implémenté."""
        return {}

    def get_leaderboard_data(self) -> LeaderboardData:
        """Retourne les données du leaderboard."""
        from core.services import leaderboard_service

        return LeaderboardData(
            current_username=user_service.get_current_username(self.current_user_id),
            entries=leaderboard_service.get_leaderboard(),
        )

    def get_profile_data(self) -> ProfileData:
        """Retourne les données du profil utilisateur courant."""
        return user_service.get_profile_data(self.current_user_id)

    def get_shop_data(self) -> ShopData:
        """Retourne les données nécessaires à la boutique."""
        return shop_service.get_shop_data(self.current_user_id)

    def buy_shop_item(self, item_id: int) -> PurchaseResult:
        """Tente l'achat d'un objet boutique pour l'utilisateur courant."""
        return shop_service.buy_item(self.current_user_id, item_id)

    def activate_shop_item(self, item_id: int) -> ActivationResult:
        """Tente l'activation d'un objet possédé pour l'utilisateur courant."""
        return shop_service.activate_owned_item(self.current_user_id, item_id)

    def get_statistics_data(self) -> StatisticsData:
        """Retourne les statistiques globales affichées dans la vue dédiée."""
        return statistics_service.get_statistics_data(self.current_user_id)
    def get_library_data(self) -> dict:
        """Données pour remplir l'espace personnel de l'étudiant."""
        return {
            "my_summaries": self.library_service.get_my_summaries(self.current_user_id),
            "my_evaluations": self.library_service.get_my_evaluations(self.current_user_id)
        }

    def modify_summary(self, summary_id: int, title: str, content: str) -> tuple:
        """Envoie les modifications au back-end."""
        return self.library_service.update_my_summary(summary_id, self.current_user_id, title, content)

    def remove_summary(self, summary_id: int) -> tuple:
        """Supprime le résumé sélectionné."""
        return self.library_service.delete_my_summary(summary_id, self.current_user_id)
    def publish_summary(self, course_id: str, title: str, content: str, academic_year: str) -> tuple:
        """Publie un résumé en utilisant l'ID de l'utilisateur connecté et l'année choisie."""
        return self.explorer_service.publish_summary(
            course_id, self.current_user_id, title, content, academic_year
        )

    def rate_summary(self, summary_id: int, rating: int, comment: str) -> tuple:
        """Evalue un résumé en utilisant l ID de l utilisateur connecté."""
        return self.explorer_service.evaluate_summary(
            summary_id, self.current_user_id, rating, comment
        )
    def get_academic_years(self) -> list:
        """Récupère les années académiques pour la liste déroulante."""
        return self.explorer_service.get_academic_years()
