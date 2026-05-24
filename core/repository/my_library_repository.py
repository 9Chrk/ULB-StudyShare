"""Requêtes SQL liées à 'my library"."""

from typing import List

from core.models.my_library import LibrarySummary
from core.models.my_library import ReceivedEvaluation


def get_user_summaries(cursor, user_id: int) -> List[LibrarySummary]:
    """Récupère la liste des résumé que l utilisateur a publié."""
    cursor.execute(
        """
        SELECT r.idResume,
               r.titre,
               r.codeCours,
               r.description,
               r.datePublication,
               COALESCE(
                   (SELECT AVG(note) FROM Evalue WHERE idResume = r.idResume),
                   0
               ) AS moyenne
          FROM Resume r
         WHERE r.idUtilisateur = %s
         ORDER BY r.datePublication DESC
        """,
        (user_id,),
    )

    return [
        LibrarySummary(
            summary_id=row[0],
            title=row[1],
            course_code=row[2],
            description=row[3],
            publication_date=row[4],
            average_rating=float(row[5]),
        )
        for row in cursor.fetchall()
    ]


def update_user_summary(
    cursor, summary_id: int, user_id: int, title: str, content: str
) -> bool:
    """Modifie le titre et le contenu d un résumé."""
    cursor.execute(
        """
        UPDATE Resume
        SET titre = %s, description = %s
        WHERE idResume = %s AND idUtilisateur = %s
        """,
        (title, content, summary_id, user_id),
    )
    return cursor.rowcount > 0


def delete_user_summary(cursor, summary_id: int, user_id: int) -> bool:
    """Supprime définitivement un résumé."""
    cursor.execute(
        """
        DELETE FROM Resume WHERE idResume = %s AND idUtilisateur = %s
        """,
        (summary_id, user_id),
    )
    return cursor.rowcount > 0


def get_evaluations_received(cursor, user_id: int) -> List[ReceivedEvaluation]:
    """Récupère les notes et commentaire reçus par l utilisateur."""
    cursor.execute(
        """
        SELECT r.titre, e.note, e.commentaire, u.nomUtilisateur
        FROM Evalue e
        JOIN Resume r ON e.idResume = r.idResume
        JOIN Utilisateur u ON e.idUtilisateur = u.idUtilisateur
        WHERE r.idUtilisateur = %s
        ORDER BY e.dateEvaluation DESC
        """,
        (user_id,),
    )

    return [
        ReceivedEvaluation(
            summary_title=row[0],
            rating=row[1],
            comment=row[2],
            evaluator_name=row[3],
        )
        for row in cursor.fetchall()
    ]
