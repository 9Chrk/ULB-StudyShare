"""Services métier liés au leaderboard."""

from typing import List, Tuple

from core.db.manager import DBManager
from core.repository.leaderboard_repository import get_top_users


def get_leaderboard(limit: int = 10) -> List[Tuple]:
    """Renvoie le classement des utilisateurs."""
    with DBManager() as cursor:
        return get_top_users(cursor, limit)
