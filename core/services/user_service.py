"""Services métier liés à l'utilisateur connecté."""

from typing import Optional

from core.db.manager import DBManager
from core.models.user import DashboardActivity
from core.models.user import DashboardData
from core.models.user import PointTransaction
from core.models.user import ProfileData
from core.models.user import UserInfo
from core.repository.user_repository import (
    get_active_title,
    get_point_transactions,
    get_recent_activity,
    get_user_info,
)


def get_current_username(user_id: Optional[int]) -> str:
    """Renvoie le nom d'utilisateur lié à user_id, ou Invité en fallback."""
    if not user_id:
        return "Invité"

    with DBManager() as cursor:
        user_info = get_user_info(cursor, user_id)
        return user_info.username if user_info else "Invité"


def get_user_profile(user_id: Optional[int]) -> Optional[UserInfo]:
    """Renvoie les infos complètes du profil, ou None."""
    if not user_id:
        return None
    with DBManager() as cursor:
        return get_user_info(cursor, user_id)


def get_dashboard_info(user_id: Optional[int]) -> DashboardData:
    """Renvoie toutes les données nécessaires au tableau de bord."""
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
    """Renvoie les données nécessaires à la vue profil."""
    if not user_id:
        return ProfileData(user_id=None, profile=None, point_transactions=[])

    with DBManager() as cursor:
        profile = get_user_info(cursor, user_id)
        transaction_rows = get_point_transactions(cursor, user_id)
        transactions = [
            PointTransaction(
                transaction_date=row[0],
                nature=row[1],
                reason=row[2],
                amount=row[3],
            )
            for row in transaction_rows
        ]

    return ProfileData(
        user_id=user_id,
        profile=profile,
        point_transactions=transactions,
    )
