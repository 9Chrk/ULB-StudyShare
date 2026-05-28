"""Modèles de donnees lies a la bibliotheque personnelle."""

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class LibrarySummary:
    """Resume publie par l'utilisateur connecte."""

    summary_id: int
    title: str
    course_code: str
    description: str
    publication_date: date
    average_rating: float


@dataclass(frozen=True)
class ReceivedEvaluation:
    """Evaluation recue sur un resume de l'utilisateur connecte."""

    summary_title: str
    rating: int
    comment: Optional[str]
    evaluator_name: str


@dataclass(frozen=True)
class MyLibraryData:
    """Donnees necessaires a la vue bibliotheque personnelle."""

    user_id: Optional[int]
    summaries: list[LibrarySummary]
    evaluations: list[ReceivedEvaluation]


@dataclass(frozen=True)
class LibraryActionResult:
    """Résultat d'une action sur un resume de la bibliotheque."""

    success: bool
    message: str
