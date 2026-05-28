"""Services métier liés à l'utilisateur connecté."""

from typing import Optional

from core.db.manager import DBManager
from core.models.user import DashboardActivity
from core.models.user import DashboardData
from core.models.user import ProfileData
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


def get_dashboard_info(user_id: Optional[int]) -> DashboardData:
    """Renvoie toutes les donnees necessaires au dashboard."""
    if not user_id:
        return DashboardData(profile=None, active_title=None, recent_activity=[])

    with DBManager() as cursor:
        profile = get_user_info(cursor, user_id)
        title = get_active_title(cursor, user_id)
        activity_rows = get_recent_activity(cursor, user_id)
        activity = [
            DashboardActivity(activity_type=row[0], title=row[1], activity_date=row[2])
            for row in activity_rows
        ]
        return DashboardData(
            profile=profile, active_title=title, recent_activity=activity
        )


def get_profile_data(user_id: Optional[int]) -> ProfileData:
    """Renvoie les données necessaires à la vue profil."""
    return ProfileData(user_id=user_id, profile=get_user_profile(user_id))
