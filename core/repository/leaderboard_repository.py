"""Requêtes SQL liées au leaderboard."""

from typing import List, Tuple


def get_top_users(cursor, limit: int = 10) -> List[Tuple]:
    """Renvoie les utilisateurs classés par points décroissants."""
    cursor.execute(
        """
        SELECT nomUtilisateur, nombrePoints, niveau
        FROM Utilisateur
        ORDER BY nombrePoints DESC
        LIMIT %s
        """,
        (limit,)
    )
    return cursor.fetchall()
