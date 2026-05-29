"""Services métier liés à l'explorateur de cours."""

from typing import Optional

from mysql.connector import Error, IntegrityError

from core.db.manager import DBManager
from core.models.explorer import ExplorerActionResult
from core.models.explorer import ExplorerData
from core.repository import explorer_repository as repository


def get_explorer_data(
    search_query: Optional[str] = None,
    selected_course_code: Optional[str] = None,
) -> ExplorerData:
    """Renvoie les cours, années et résumés de la sélection courante."""
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


def add_course(
    code: str, name: str, faculty: str, credits: str
) -> ExplorerActionResult:
    """Ajoute un cours dans le catalogue."""
    code = code.strip().upper()
    name = name.strip()
    faculty = faculty.strip()
    credits = credits.strip()

    if not code or not name or not faculty or not credits:
        return ExplorerActionResult(
            False, "Code, nom, faculté et crédits obligatoires."
        )

    try:
        credits_value = int(credits)
    except ValueError:
        return ExplorerActionResult(False, "Le nombre de crédits doit être entier.")

    if credits_value < 1:
        return ExplorerActionResult(
            False, "Le nombre de crédits doit être supérieur ou égal à 1."
        )

    try:
        with DBManager() as cursor:
            repository.insert_course(cursor, code, name, faculty, credits_value)

    except IntegrityError:
        return ExplorerActionResult(False, "Ce cours existe déjà.")

    except Error:
        return ExplorerActionResult(
            False, "Impossible d'ajouter le cours pour le moment."
        )

    return ExplorerActionResult(True, "Cours ajouté avec succès.")


def publish_summary(
    user_id: Optional[int],
    course_code: Optional[str],
    title: str,
    content: str,
    academic_year: str,
) -> ExplorerActionResult:
    """Publie un résumé et attribue les points associés."""
    if not user_id:
        return ExplorerActionResult(False, "Utilisateur non connecté.")

    course_code = (course_code or "").strip()
    title = title.strip()
    content = content.strip()
    academic_year = academic_year.strip()

    if not course_code:
        return ExplorerActionResult(False, "Sélectionnez un cours.")

    if not title or not content or not academic_year:
        return ExplorerActionResult(False, "Tous les champs sont obligatoires.")

    try:
        with DBManager() as cursor:
            repository.insert_summary(
                cursor, course_code, user_id, title, content, academic_year
            )
            repository.award_points(cursor, user_id, 10, "Publication de résumé")

    except IntegrityError:
        return ExplorerActionResult(
            False, "Publication impossible pour ce cours ou cette année."
        )

    except Error:
        return ExplorerActionResult(False, "Publication impossible pour le moment.")

    return ExplorerActionResult(True, "Résumé publié. +10 points.")


def evaluate_summary(
    user_id: Optional[int], summary_id: int, rating: int, comment: str
) -> ExplorerActionResult:
    """Ajoute une évaluation sur un résumé public."""
    if not user_id:
        return ExplorerActionResult(False, "Utilisateur non connecté.")

    if not 1 <= rating <= 5:
        return ExplorerActionResult(False, "La note doit être comprise entre 1 et 5.")

    comment = comment.strip()

    try:
        with DBManager() as cursor:
            author_id = repository.get_summary_author_id(cursor, summary_id)
            if author_id is None:
                return ExplorerActionResult(False, "Résumé introuvable.")
            if author_id == user_id:
                return ExplorerActionResult(
                    False, "Vous ne pouvez pas évaluer votre propre résumé."
                )
            if repository.check_already_evaluated(cursor, summary_id, user_id):
                return ExplorerActionResult(False, "Vous avez déjà évalué ce résumé.")

            repository.insert_evaluation(cursor, summary_id, user_id, rating, comment)
            repository.award_points(cursor, author_id, 2, "Évaluation reçue")

    except IntegrityError:
        return ExplorerActionResult(False, "Évaluation impossible pour ce résumé.")

    except Error:
        return ExplorerActionResult(False, "Évaluation impossible pour le moment.")

    return ExplorerActionResult(
        True, "Évaluation enregistrée. L'auteur reçoit +2 points."
    )
