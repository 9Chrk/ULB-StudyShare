"""Modeles de donnees lies aux statistiques globales."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class TopUserStat:
    username: str
    points: int
    level: int


@dataclass(frozen=True)
class MultiCourseUserStat:
    username: str
    course_count: int
    resume_count: int


@dataclass(frozen=True)
class TopCourseStat:
    code: str
    name: str
    resume_count: int


@dataclass(frozen=True)
class BestRatedResumeStat:
    course_code: str
    course_name: str
    resume_title: str
    average_rating: float


@dataclass(frozen=True)
class UserWithoutResumeStat:
    username: str
    email: str
    points: int


@dataclass(frozen=True)
class MostBoughtCosmeticStat:
    item_id: int
    name: str
    description: str
    price_points: int
    purchase_count: int


@dataclass(frozen=True)
class OverspendingUserStat:
    username: str
    points: int
    total_spent: int
    excess_spent: int


@dataclass(frozen=True)
class StatisticsData:
    """Agregat des statistiques affichees dans la vue."""

    top_users: list[TopUserStat]
    multi_course_users: list[MultiCourseUserStat]
    top_courses: list[TopCourseStat]
    best_rated_resumes: list[BestRatedResumeStat]
    users_without_resumes: list[UserWithoutResumeStat]
    most_bought_cosmetics: list[MostBoughtCosmeticStat]
    overspending_users: list[OverspendingUserStat]
    average_resumes_per_user: Optional[float]
