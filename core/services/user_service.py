"""Services métier liés à l'utilisateur connecté."""

from typing import Optional

from core.db.manager import DBManager
from core.repository.user_repository import get_user_info
from core.repository.user_repository import get_active_title, get_recent_activity


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

def get_dashboard_info(user_id: Optional[int]) -> dict:
    """Renvoie toutes les données nécessaires au dashboard."""
    if not user_id:
        return {}
    with DBManager() as cursor:
        profile = get_user_info(cursor, user_id)
        title = get_active_title(cursor, user_id)
        activity = get_recent_activity(cursor, user_id)
        return {
            "profile": profile,
            "active_title": title,
            "recent_activity": activity,
        }
