"""Modèles de données liés aux statistiques globales."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class TopUserStat:
    """Statistique d'un utilisateur classé parmi les meilleurs points."""

    username: str
    points: int
    level: int


@dataclass(frozen=True)
class MultiCourseUserStat:
    """Statistique d'un utilisateur ayant publié sur plusieurs cours."""

    username: str
    course_count: int
    resume_count: int


@dataclass(frozen=True)
class TopCourseStat:
    """Statistique d'un cours selon son volume de résumés publiés."""

    code: str
    name: str
    resume_count: int


@dataclass(frozen=True)
class BestRatedResumeStat:
    """Statistique d'un résumé ayant la meilleure note moyenne pour un cours."""

    course_code: str
    course_name: str
    resume_title: str
    average_rating: float


@dataclass(frozen=True)
class UserWithoutResumeStat:
    """Statistique d'un utilisateur n'ayant encore publié aucun résumé."""

    username: str
    email: str
    points: int


@dataclass(frozen=True)
class MostBoughtCosmeticStat:
    """Statistique d'un objet cosmétique selon son nombre d'achats."""

    item_id: int
    name: str
    description: str
    price_points: int
    purchase_count: int


@dataclass(frozen=True)
class OverspendingUserStat:
    """Statistique d'un utilisateur ayant dépensé plus de points qu'il n'en avait."""

    username: str
    points: int
    total_spent: int
    excess_spent: int


@dataclass(frozen=True)
class StatisticsData:
    """Agrégat des statistiques affichées dans la vue."""

    top_users: list[TopUserStat]
    multi_course_users: list[MultiCourseUserStat]
    top_courses: list[TopCourseStat]
    best_rated_resumes: list[BestRatedResumeStat]
    users_without_resumes: list[UserWithoutResumeStat]
    most_bought_cosmetics: list[MostBoughtCosmeticStat]
    overspending_users: list[OverspendingUserStat]
    average_resumes_per_user: Optional[float]
