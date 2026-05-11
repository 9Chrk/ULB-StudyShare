"""Requêtes SQL liées au leaderboard."""

from typing import List, Optional, Tuple


def get_top_users(cursor, limit: Optional[int] = None) -> List[Tuple]:
    """Renvoie les utilisateurs classés par points décroissants."""
    query = """
        SELECT nomUtilisateur, nombrePoints, niveau
        FROM Utilisateur
        ORDER BY nombrePoints DESC
    """

    if limit is not None:
        query += " LIMIT %s"
        cursor.execute(query, (limit,))
    else:
        cursor.execute(query)

    return cursor.fetchall()
