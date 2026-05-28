"""Services metier lies a l'explorateur de cours."""

from typing import Optional

from mysql.connector import IntegrityError

from core.db.manager import DBManager
from core.models.explorer import ExplorerActionResult
from core.models.explorer import ExplorerData
from core.repository import explorer_repository as repository


def get_explorer_data(
    search_query: Optional[str] = None,
    selected_course_code: Optional[str] = None,
) -> ExplorerData:
    """Renvoie les cours, années et resumes de la selection courante."""
    query = (search_query or "").strip()
    course_code = (selected_course_code or "").strip() or None

    with DBManager() as cursor:
        courses = (
            repository.search_courses(cursor, query)
            if query
            else repository.get_all_courses(cursor)
        )
        summaries = (
            repository.get_summaries_by_course(cursor, course_code)
            if course_code
            else []
        )
        academic_years = repository.get_academic_years(cursor)

    return ExplorerData(
        courses=courses,
        summaries=summaries,
        academic_years=academic_years,
        selected_course_code=course_code,
    )


def add_course(code: str, name: str, faculty: str) -> ExplorerActionResult:
    """Ajoute un cours dans le catalogue."""
    code = code.strip().upper()
    name = name.strip()
    faculty = faculty.strip()

    if not code or not name or not faculty:
        return ExplorerActionResult(False, "Code, nom et faculté obligatoires.")

    try:
        with DBManager() as cursor:
            repository.insert_course(cursor, code, name, faculty)

    except IntegrityError:
        return ExplorerActionResult(False, "Ce cours existe deja.")

    return ExplorerActionResult(True, "Cours ajoute avec succès.")


def publish_summary(
    user_id: Optional[int],
    course_code: Optional[str],
    title: str,
    content: str,
    academic_year: str,
) -> ExplorerActionResult:
    """Publie un resume et attribue les points associés."""
    if not user_id:
        return ExplorerActionResult(False, "Utilisateur non connecte.")

    course_code = (course_code or "").strip()
    title = title.strip()
    content = content.strip()
    academic_year = academic_year.strip()

    if not course_code:
        return ExplorerActionResult(False, "Selectionnez un cours.")
    if not title or not content or not academic_year:
        return ExplorerActionResult(False, "Tous les champs sont obligatoires.")

    try:
        with DBManager() as cursor:
            repository.insert_summary(
                cursor, course_code, user_id, title, content, academic_year
            )
            repository.award_points(cursor, user_id, 10, "Publication resume")
    except IntegrityError:
        return ExplorerActionResult(
            False, "Publication impossible pour ce cours ou cette année."
        )

    return ExplorerActionResult(True, "Resume publie. +10 points.")


def evaluate_summary(
    user_id: Optional[int], summary_id: int, rating: int, comment: str
) -> ExplorerActionResult:
    """Ajoute une evaluation sur un resume public."""
    if not user_id:
        return ExplorerActionResult(False, "Utilisateur non connecte.")
    if not 1 <= rating <= 5:
        return ExplorerActionResult(False, "La note doit être comprise entre 1 et 5.")

    comment = comment.strip()

    try:
        with DBManager() as cursor:
            author_id = repository.get_summary_author_id(cursor, summary_id)
            if author_id is None:
                return ExplorerActionResult(False, "Resume introuvable.")
            if author_id == user_id:
                return ExplorerActionResult(
                    False, "Vous ne pouvez pas evaluer votre propre resume."
                )
            if repository.check_already_evaluated(cursor, summary_id, user_id):
                return ExplorerActionResult(False, "Vous avez deja évalué ce resume.")

            repository.insert_evaluation(cursor, summary_id, user_id, rating, comment)
            repository.award_points(cursor, user_id, 2, "Evaluation resume")
    except IntegrityError:
        return ExplorerActionResult(False, "Evaluation impossible pour ce resume.")

    return ExplorerActionResult(True, "Evaluation enregistrée. +2 points.")
