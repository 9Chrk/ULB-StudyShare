"""Modèles de données liés à l'explorateur de cours."""

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class CourseInfo:
    """Cours affiché dans l'explorateur."""

    code: str
    name: str
    faculty: str
    credits: int


@dataclass(frozen=True)
class ExplorerSummary:
    """Résumé public associé à un cours."""

    summary_id: int
    title: str
    description: str
    author: str
    publication_date: date
    average_rating: float
    evaluation_count: int


@dataclass(frozen=True)
class ExplorerData:
    """Données nécessaires à la vue explorateur."""

    courses: list[CourseInfo]
    summaries: list[ExplorerSummary]
    academic_years: list[str]
    selected_course_code: Optional[str]


@dataclass(frozen=True)
class ExplorerActionResult:
    """Résultat d'une action réalisée depuis l'explorateur."""

    success: bool
    message: str
