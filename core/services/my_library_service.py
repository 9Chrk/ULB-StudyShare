"""Services metier lies a la bibliotheque personnelle."""

from typing import Optional

from core.db.manager import DBManager
from core.models.my_library import LibraryActionResult
from core.models.my_library import MyLibraryData
from core.repository import my_library_repository as repository


def get_my_library_data(user_id: Optional[int]) -> MyLibraryData:
    """Renvoie les resumes et evaluations de l'utilisateur connecte."""
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
    """Modifie le titre et la description d'un resume possede."""
    if not user_id:
        return LibraryActionResult(False, "Utilisateur non connecté.")

    title = title.strip()
    content = content.strip()
    if not title or not content:
        return LibraryActionResult(
            False, "Le titre et la description ne peuvent pas être vides."
        )

    with DBManager() as cursor:
        success = repository.update_user_summary(
            cursor, summary_id, user_id, title, content
        )

    if success:
        return LibraryActionResult(True, "Votre résumé a bien été modifié.")
    return LibraryActionResult(False, "Modification impossible pour ce résumé.")


def delete_my_summary(
    user_id: Optional[int], summary_id: int
) -> LibraryActionResult:
    """Supprime un resume possede par l'utilisateur connecte."""
    if not user_id:
        return LibraryActionResult(False, "Utilisateur non connecté.")

    with DBManager() as cursor:
        success = repository.delete_user_summary(cursor, summary_id, user_id)

    if success:
        return LibraryActionResult(True, "Résumé supprimé définitivement.")
    return LibraryActionResult(False, "Impossible de supprimer ce résumé.")
