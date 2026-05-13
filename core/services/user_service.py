"""Services métier liés à l'utilisateur connecté."""

from typing import Optional

from core.db.manager import DBManager
from core.repository.user_repository import get_user_info


def get_current_username(user_id: Optional[int]) -> str:
    """Renvoie le nom d'utilisateur lié à user_id, ou Guest en fallback."""
    if not user_id:
        return "Guest"

    with DBManager() as cursor:
        user_info = get_user_info(cursor, user_id)
        return user_info.username if user_info else "Guest"


def get_user_profile(user_id: Optional[int]):
    """Renvoie les infos complètes du profil, ou None."""
    if not user_id:
        return None
    with DBManager() as cursor:
        return get_user_info(cursor, user_id)
