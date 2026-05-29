"""Services métier liés à la bibliothèque personnelle."""

from typing import Optional

from mysql.connector import Error

from core.db.manager import DBManager
from core.models.my_library import LibraryActionResult
from core.models.my_library import MyLibraryData
from core.repository import my_library_repository as repository


def get_my_library_data(user_id: Optional[int]) -> MyLibraryData:
    """Renvoie les résumés et évaluations de l'utilisateur connecté."""
    if not user_id:
        return MyLibraryData(user_id=None, summaries=[], evaluations=[])

    with DBManager() as cursor:
        summaries = repository.get_user_summaries(cursor, user_id)
        evaluations = repository.get_evaluations_received(cursor, user_id)

    return MyLibraryData(
        user_id=user_id,
        summaries=summaries,
        evaluations=evaluations,
    )


def update_my_summary(
    user_id: Optional[int], summary_id: int, title: str, content: str
) -> LibraryActionResult:
    """Modifie le titre et la description d'un résumé possédé."""
    if not user_id:
        return LibraryActionResult(False, "Utilisateur non connecté.")

    title = title.strip()
    content = content.strip()

    if not title or not content:
        return LibraryActionResult(
            False, "Le titre et la description ne peuvent pas être vides."
        )

    try:
        with DBManager() as cursor:
            success = repository.update_user_summary(
                cursor, summary_id, user_id, title, content
            )
    except Error:
        return LibraryActionResult(False, "Modification impossible pour le moment.")

    if success:
        return LibraryActionResult(True, "Votre résumé a bien été modifié.")

    return LibraryActionResult(False, "Modification impossible pour ce résumé.")


def delete_my_summary(
    user_id: Optional[int], summary_id: int
) -> LibraryActionResult:
    """Supprime un résumé possédé par l'utilisateur connecté."""
    if not user_id:
        return LibraryActionResult(False, "Utilisateur non connecté.")

    try:
        with DBManager() as cursor:
            success = repository.delete_user_summary(cursor, summary_id, user_id)

    except Error:
        return LibraryActionResult(False, "Suppression impossible pour le moment.")

    if success:
        return LibraryActionResult(True, "Résumé supprimé définitivement.")

    return LibraryActionResult(False, "Impossible de supprimer ce résumé.")
