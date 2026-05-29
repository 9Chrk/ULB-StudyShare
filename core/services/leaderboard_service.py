"""Services métier liés au classement."""

from typing import Optional

from core.db.manager import DBManager
from core.models.leaderboard import LeaderboardEntry
from core.repository.leaderboard_repository import get_top_users


def get_leaderboard(limit: Optional[int] = None) -> list[LeaderboardEntry]:
    """Renvoie le classement complet des utilisateurs (tous par défaut)."""
    with DBManager() as cursor:
        rows = get_top_users(cursor, limit)
        return [
            LeaderboardEntry(username=row[0], points=row[1], level=row[2])
            for row in rows
        ]
