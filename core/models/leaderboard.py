"""Modèles de données liés au leaderboard."""

from dataclasses import dataclass


@dataclass(frozen=True)
class LeaderboardEntry:
    """Ligne du classement utilisateur."""

    username: str
    points: int
    level: int


@dataclass(frozen=True)
class LeaderboardData:
    """Données nécessaires à la vue classement."""

    current_username: str
    entries: list[LeaderboardEntry]
