"""Contrôleur principal de l'application."""

from collections.abc import Callable

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


class AppController:
    """Contrôle la navigation entre les écrans."""

    def __init__(self, root):
        """Conserve la fenêtre racine et instancie les contrôleurs spécialisés."""
        self.root = root

        # utilisateur connecté
        self.current_user_id = None
        self._refresh_listeners: list[Callable[[], None]] = []

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

    # ---------- FONCTIONS DE RAFRAÎCHISSEMENT GLOBAL ----------

    def subscribe_refresh(self, callback: Callable[[], None]) -> None:
        """Ajoute un observateur appelé quand les données applicatives changent."""
        if callback not in self._refresh_listeners:
            self._refresh_listeners.append(callback)

    def unsubscribe_refresh(self, callback: Callable[[], None]) -> None:
        """Retire un observateur de rafraîchissement."""
        if callback in self._refresh_listeners:
            self._refresh_listeners.remove(callback)

    def refresh(self) -> None:
        """Recharge les vues abonnées après une mutation de données."""
        for callback in list(self._refresh_listeners):
            callback()
    
    # ---------- FONCTIONS DE GESTION DE LA BOUTIQUE ----------
    
    def buy_shop_item(self, item_id: int) -> PurchaseResult:
        """Tente l'achat d'un objet boutique pour l'utilisateur courant."""
        result = shop_service.buy_item(self.current_user_id, item_id)
        if result.success:
            self.refresh()
        return result

    def activate_shop_item(self, item_id: int) -> ActivationResult:
        """Tente l'activation d'un objet possédé pour l'utilisateur courant."""
        result = shop_service.activate_owned_item(self.current_user_id, item_id)
        if result.success:
            self.refresh()
        return result
    
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

    def get_my_library_data(self) -> dict:
        """Retourne les données de la bibliothèque personnelle, encore non implémenté."""
        return {}

    def get_profile_data(self) -> ProfileData:
        """Retourne les données du profil utilisateur courant."""
        return user_service.get_profile_data(self.current_user_id)

    def get_shop_data(self) -> ShopData:
        """Retourne les données nécessaires à la boutique."""
        return shop_service.get_shop_data(self.current_user_id)

    def get_statistics_data(self) -> StatisticsData:
        """Retourne les statistiques globales affichées dans la vue dédiée."""
        return statistics_service.get_statistics_data(self.current_user_id)
