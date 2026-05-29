"""Modèles de données liés aux utilisateurs."""

from dataclasses import dataclass
from datetime import date, datetime
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
    """Activité récente affichée sur le dashboard."""

    activity_type: str
    title: str
    activity_date: date


@dataclass(frozen=True)
class DashboardData:
    """Données nécessaires à la vue tableau de bord."""

    profile: Optional[UserInfo]
    active_title: Optional[str]
    recent_activity: list[DashboardActivity]


@dataclass(frozen=True)
class PointTransaction:
    """Transaction de points affichée dans l'historique du profil."""

    transaction_date: datetime
    nature: str
    reason: str
    amount: int


@dataclass(frozen=True)
class ProfileData:
    """Données nécessaires à la vue profil."""

    user_id: Optional[int]
    profile: Optional[UserInfo]
    point_transactions: list[PointTransaction]
