"""Services métier liés au leaderboard."""

from typing import List, Optional, Tuple

from core.db.manager import DBManager
from core.repository.leaderboard_repository import get_top_users


def get_leaderboard(limit: Optional[int] = None) -> List[Tuple]:
    """Renvoie le classement complet des utilisateurs (tous par défaut)."""
    with DBManager() as cursor:
        return get_top_users(cursor, limit)
