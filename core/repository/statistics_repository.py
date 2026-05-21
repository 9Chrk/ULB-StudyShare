"""Requêtes SQL liées aux statistiques globales."""

from typing import List, Optional, Tuple


def get_top_users_by_points(cursor, limit: int = 10) -> List[Tuple]:
    cursor.execute(
        """
        SELECT nomUtilisateur, nombrePoints, niveau
        FROM Utilisateur
        ORDER BY nombrePoints DESC, nomUtilisateur ASC
        LIMIT %s
        """,
        (limit,),
    )
    return cursor.fetchall()


def get_users_with_at_least_n_courses(cursor, min_courses: int = 3) -> List[Tuple]:
    cursor.execute(
        """
        SELECT u.nomUtilisateur, COUNT(DISTINCT r.codeCours) AS nb_cours, COUNT(r.idResume) AS nb_resumes
        FROM Utilisateur u
        JOIN Resume r ON r.idUtilisateur = u.idUtilisateur
        GROUP BY u.idUtilisateur, u.nomUtilisateur
        HAVING COUNT(DISTINCT r.codeCours) >= %s
        ORDER BY nb_cours DESC, nb_resumes DESC, u.nomUtilisateur ASC
        """,
        (min_courses,),
    )
    return cursor.fetchall()


def get_courses_with_most_resumes(cursor) -> List[Tuple]:
    cursor.execute(
        """
        SELECT c.codeCours, c.nomCours, COUNT(r.idResume) AS nb_resumes
        FROM Cours c
        LEFT JOIN Resume r ON r.codeCours = c.codeCours
        GROUP BY c.codeCours, c.nomCours
        ORDER BY nb_resumes DESC, c.nomCours ASC
        """,
    )
    return cursor.fetchall()


def get_best_rated_resumes_by_course(cursor) -> List[Tuple]:
    cursor.execute(
        """
        SELECT rr.codeCours, rr.nomCours, rr.titre, rr.avg_note
        FROM (
            SELECT
                c.codeCours,
                c.nomCours,
                r.idResume,
                r.titre,
                AVG(e.note) AS avg_note
            FROM Resume r
            JOIN Cours c ON c.codeCours = r.codeCours
            JOIN Evalue e ON e.idResume = r.idResume
            GROUP BY c.codeCours, c.nomCours, r.idResume, r.titre
        ) AS rr
        JOIN (
            SELECT codeCours, MAX(avg_note) AS best_avg
            FROM (
                SELECT
                    c.codeCours,
                    r.idResume,
                    AVG(e.note) AS avg_note
                FROM Resume r
                JOIN Cours c ON c.codeCours = r.codeCours
                JOIN Evalue e ON e.idResume = r.idResume
                GROUP BY c.codeCours, r.idResume
            ) AS averages
            GROUP BY codeCours
        ) AS best_per_course
          ON best_per_course.codeCours = rr.codeCours
         AND best_per_course.best_avg = rr.avg_note
        ORDER BY rr.nomCours ASC, rr.titre ASC
        """,
    )
    return cursor.fetchall()


def get_users_with_no_resumes(cursor) -> List[Tuple]:
    cursor.execute(
        """
        SELECT u.nomUtilisateur, u.email, u.nombrePoints
        FROM Utilisateur u
        LEFT JOIN Resume r ON r.idUtilisateur = u.idUtilisateur
        WHERE r.idResume IS NULL
        ORDER BY u.nomUtilisateur ASC
        """,
    )
    return cursor.fetchall()


def get_most_bought_cosmetics(cursor) -> List[Tuple]:
    cursor.execute(
        """
        SELECT oc.idObjet, oc.nomObjet, oc.description, oc.prixPoints, COUNT(p.idObjet) AS purchase_count
        FROM ObjetCosmetique oc
        LEFT JOIN Possede p ON p.idObjet = oc.idObjet
        GROUP BY oc.idObjet, oc.nomObjet, oc.description, oc.prixPoints
        ORDER BY purchase_count DESC, oc.nomObjet ASC
        LIMIT 1
        """,
    )
    return cursor.fetchall()


def get_users_spending_more_than_available(cursor) -> List[Tuple]:
    cursor.execute(
        """
        SELECT
            u.nomUtilisateur,
            u.nombrePoints,
            COALESCE(SUM(tp.montantPoints), 0) AS total_spent,
            COALESCE(SUM(tp.montantPoints), 0) - u.nombrePoints AS excess_spent
        FROM Utilisateur u
        LEFT JOIN TransactionPoints tp
            ON tp.idUtilisateur = u.idUtilisateur
           AND tp.natureTransaction = 'depense'
        GROUP BY u.idUtilisateur, u.nomUtilisateur, u.nombrePoints
        HAVING COALESCE(SUM(tp.montantPoints), 0) > u.nombrePoints
        ORDER BY excess_spent DESC, total_spent DESC, u.nomUtilisateur ASC
        """,
    )
    return cursor.fetchall()


def get_average_resumes_per_user(cursor) -> Optional[float]:
    cursor.execute(
        """
        SELECT AVG(user_resume_count)
        FROM (
            SELECT u.idUtilisateur, COUNT(r.idResume) AS user_resume_count
            FROM Utilisateur u
            LEFT JOIN Resume r ON r.idUtilisateur = u.idUtilisateur
            GROUP BY u.idUtilisateur
        ) AS per_user
        """,
    )
    row = cursor.fetchone()
    return float(row[0]) if row and row[0] is not None else None
