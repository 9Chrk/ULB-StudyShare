"""Modèles de données liés à la bibliothèque personnelle."""

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class LibrarySummary:
    """Résumé publié par l'utilisateur connecté."""

    summary_id: int
    title: str
    course_code: str
    description: str
    publication_date: date
    average_rating: float


@dataclass(frozen=True)
class ReceivedEvaluation:
    """Évaluation reçue sur un résumé de l'utilisateur connecté."""

    summary_title: str
    rating: int
    comment: Optional[str]
    evaluator_name: str


@dataclass(frozen=True)
class MyLibraryData:
    """Données nécessaires à la vue bibliothèque personnelle."""

    user_id: Optional[int]
    summaries: list[LibrarySummary]
    evaluations: list[ReceivedEvaluation]


@dataclass(frozen=True)
class LibraryActionResult:
    """Résultat d'une action sur un résumé de la bibliothèque."""

    success: bool
    message: str
