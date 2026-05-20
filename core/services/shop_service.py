"""Services métier liés à la boutique."""

from typing import Optional

from core.db.manager import DBManager
from core.models.shop import ActivationResult
from core.models.shop import PurchaseResult
from core.repository.shop_repository import activate_item
from core.repository.shop_repository import add_owned_item
from core.repository.shop_repository import create_spend_transaction
from core.repository.shop_repository import get_catalogue
from core.repository.shop_repository import get_item_by_id
from core.repository.shop_repository import get_owned_item_ids
from core.repository.shop_repository import get_user_shop_state
from core.repository.shop_repository import is_item_owned
from core.repository.shop_repository import spend_user_points


def get_shop_data(user_id: Optional[int]) -> dict:
    """Renvoie le catalogue, inventaire, points et objets actifs."""
    if not user_id:
        return {
            "catalogue": [],
            "owned": [],
            "points": 0,
            "active_badge_id": None,
            "active_title_id": None,
            "active_theme_id": None,
        }

    with DBManager() as cursor:
        catalogue = get_catalogue(cursor)
        owned = get_owned_item_ids(cursor, user_id)
        state = get_user_shop_state(cursor, user_id)

        if state is None:
            return {
                "catalogue": catalogue,
                "owned": owned,
                "points": 0,
                "active_badge_id": None,
                "active_title_id": None,
                "active_theme_id": None,
            }

        return {
            "catalogue": catalogue,
            "owned": owned,
            "points": state.points,
            "active_badge_id": state.active_badge_id,
            "active_title_id": state.active_title_id,
            "active_theme_id": state.active_theme_id,
        }


def buy_item(user_id: Optional[int], item_id: int) -> PurchaseResult:
    """Achète un objet cosmétique si l'utilisateur possède assez de points."""
    if not user_id:
        return PurchaseResult(False, "Utilisateur non connecté.")

    with DBManager() as cursor:
        item = get_item_by_id(cursor, item_id)
        if item is None:
            return PurchaseResult(False, "Objet introuvable.")

        if is_item_owned(cursor, user_id, item_id):
            return PurchaseResult(False, "Cet objet est déjà possédé.")

        state = get_user_shop_state(cursor, user_id)
        if state is None:
            return PurchaseResult(False, "Profil utilisateur introuvable.")

        if state.points < item.price_points:
            return PurchaseResult(False, "Points insuffisants pour cet achat.")

        add_owned_item(cursor, user_id, item_id)
        spend_user_points(cursor, user_id, item.price_points)
        create_spend_transaction(cursor, user_id, item.price_points, f"Achat boutique: {item.name}")
        return PurchaseResult(True, f"Achat réussi: {item.name}.")


def activate_owned_item(user_id: Optional[int], item_id: int) -> ActivationResult:
    """Active un objet possédé (badge, titre ou thème)."""
    if not user_id:
        return ActivationResult(False, "Utilisateur non connecté.")

    with DBManager() as cursor:
        item = get_item_by_id(cursor, item_id)
        if item is None:
            return ActivationResult(False, "Objet introuvable.")

        if item.item_type not in ("badge", "titre", "theme"):
            return ActivationResult(False, "Ce type d'objet ne peut pas être activé.")

        if not is_item_owned(cursor, user_id, item_id):
            return ActivationResult(False, "Vous devez acheter cet objet avant activation.")

        if not activate_item(cursor, user_id, item_id, item.item_type):
            return ActivationResult(False, "Activation impossible.")

        return ActivationResult(True, f"{item.name} activé.")
