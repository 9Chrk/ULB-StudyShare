"""Modèles de données liés aux utilisateurs."""

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class UserInfo:
    """Données utilisateur minimales utilisées par les vues/services."""

    username: str
    email: str
    registration_date: date
    level: int
    points: int


@dataclass(frozen=True)
class DashboardActivity:
    """Activite recente affichee sur le dashboard."""

    activity_type: str
    title: str
    activity_date: date


@dataclass(frozen=True)
class DashboardData:
    """Donnees necessaires a la vue dashboard."""

    profile: Optional[UserInfo]
    active_title: Optional[str]
    recent_activity: list[DashboardActivity]


@dataclass(frozen=True)
class ProfileData:
    """Donnees necessaires a la vue profil."""

    user_id: Optional[int]
    profile: Optional[UserInfo]
