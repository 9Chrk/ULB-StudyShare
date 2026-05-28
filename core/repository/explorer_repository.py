"""Requêtes SQL liées a l'explorateur de cours."""

from typing import List, Optional

from core.models.explorer import CourseInfo
from core.models.explorer import ExplorerSummary


def get_all_courses(cursor) -> List[CourseInfo]:
    """Renvoie tous les cours triés par nom."""
    cursor.execute("SELECT codeCours, nomCours, faculte FROM Cours ORDER BY nomCours")
    return [
        CourseInfo(code=row[0], name=row[1], faculty=row[2])
        for row in cursor.fetchall()
    ]


def search_courses(cursor, query: str) -> List[CourseInfo]:
    """Recherche un cours par code, nom ou faculte."""
    like_query = f"%{query}%"
    cursor.execute(
        """
        SELECT codeCours, nomCours, faculte
        FROM Cours
        WHERE codeCours LIKE %s OR nomCours LIKE %s OR faculte LIKE %s
        ORDER BY nomCours
        """,
        (like_query, like_query, like_query),
    )
    return [
        CourseInfo(code=row[0], name=row[1], faculty=row[2])
        for row in cursor.fetchall()
    ]


def insert_course(cursor, code: str, name: str, faculty: str) -> bool:
    """Inséré un nouveau cours et signale si l'insertion a eu lieu."""
    cursor.execute(
        """
        INSERT INTO Cours (codeCours, nomCours, faculte)
        VALUES (%s, %s, %s)
        """,
        (code, name, faculty),
    )
    return cursor.rowcount > 0


def get_summaries_by_course(cursor, course_code: str) -> List[ExplorerSummary]:
    """Renvoie les resumes publics d'un cours avec leur note moyenne."""
    cursor.execute(
        """
        SELECT r.idResume,
               r.titre,
               COALESCE(r.description, ''),
               u.nomUtilisateur,
               r.datePublication,
               COALESCE(AVG(e.note), 0) AS avg_rating,
               COUNT(e.note) AS eval_count
        FROM Resume r
        JOIN Utilisateur u ON r.idUtilisateur = u.idUtilisateur
        LEFT JOIN Evalue e ON r.idResume = e.idResume
        WHERE r.codeCours = %s AND r.visibilite = 'publique'
        GROUP BY r.idResume, r.titre, r.description, u.nomUtilisateur, r.datePublication
        ORDER BY avg_rating DESC, r.datePublication DESC, r.titre ASC
        """,
        (course_code,),
    )
    return [
        ExplorerSummary(
            summary_id=row[0],
            title=row[1],
            description=row[2],
            author=row[3],
            publication_date=row[4],
            average_rating=float(row[5]),
            evaluation_count=row[6],
        )
        for row in cursor.fetchall()
    ]


def insert_summary(
    cursor, course_code: str, user_id: int, title: str, content: str, academic_year: str
) -> None:
    """Inséré un resume public pour le cours et l'annee choisis."""
    cursor.execute(
        """
        INSERT INTO Resume (titre, description, datePublication, version, visibilite, idUtilisateur, codeCours, codeAnnee)
        VALUES (%s, %s, CURRENT_DATE(), 1, 'publique', %s, %s, %s)
        """,
        (title, content, user_id, course_code, academic_year),
    )


def check_already_evaluated(cursor, summary_id: int, user_id: int) -> bool:
    """Vérifie si l'utilisateur a deja évalué ce resume."""
    cursor.execute(
        "SELECT 1 FROM Evalue WHERE idResume = %s AND idUtilisateur = %s",
        (summary_id, user_id),
    )
    return cursor.fetchone() is not None


def get_summary_author_id(cursor, summary_id: int) -> Optional[int]:
    """Renvoie l'auteur d'un resume, ou None si le resume n'existe pas."""
    cursor.execute(
        "SELECT idUtilisateur FROM Resume WHERE idResume = %s",
        (summary_id,),
    )
    row = cursor.fetchone()
    return row[0] if row else None


def insert_evaluation(
    cursor, summary_id: int, user_id: int, rating: int, comment: str
) -> None:
    """Ajoute une evaluation sur un resume."""
    cursor.execute(
        """
        INSERT INTO Evalue (idUtilisateur, idResume, note, commentaire, dateEvaluation)
        VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
        """,
        (user_id, summary_id, rating, comment or None),
    )


def award_points(cursor, user_id: int, amount: int, reason: str) -> None:
    """Crédite des points et historise la transaction."""
    cursor.execute(
        """
        UPDATE Utilisateur
        SET nombrePoints = nombrePoints + %s
        WHERE idUtilisateur = %s
        """,
        (amount, user_id),
    )
    cursor.execute(
        """
        INSERT INTO TransactionPoints (montantPoints, natureTransaction, motif, idUtilisateur)
        VALUES (%s, 'gain', %s, %s)
        """,
        (amount, reason, user_id),
    )


def get_academic_years(cursor) -> List[str]:
    """Renvoie les années académiques connues."""
    cursor.execute("SELECT codeAnnee FROM AnneeAcademique ORDER BY codeAnnee DESC")
    return [row[0] for row in cursor.fetchall()]
