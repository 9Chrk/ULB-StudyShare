"""Modeles de donnees lies au leaderboard."""

from dataclasses import dataclass


@dataclass(frozen=True)
class LeaderboardEntry:
    """Ligne du classement utilisateur."""

    username: str
    points: int
    level: int


@dataclass(frozen=True)
class LeaderboardData:
    """Donnees necessaires a la vue leaderboard."""

    current_username: str
    entries: list[LeaderboardEntry]
