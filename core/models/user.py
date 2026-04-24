"""Modèles de données liés aux utilisateurs."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class UserInfo:
    """Données utilisateur minimales utilisées par les vues/services."""

    username: str
    email: str
    registration_date: date
    level: int
    points: int
