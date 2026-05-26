"""Requêtes SQL liées à l'Explorer"""

from typing import List, Optional
from dataclasses import dataclass

@dataclass
class CourseInfo:
    code_cours: str
    nom_cours: str
    faculte: str

@dataclass
class SummaryInfo:
    id_resume: int
    titre: str
    description: str
    auteur: str
    date_pub: str
    moyenne: float
    nb_eval: int

def get_all_courses(cursor) -> List[CourseInfo]:
    cursor.execute("SELECT codeCours, nomCours, faculte FROM Cours ORDER BY nomCours")
    return [CourseInfo(r[0], r[1], r[2]) for r in cursor.fetchall()]

def search_courses(cursor, query: str) -> List[CourseInfo]:
    like_query = f"%{query}%"
    cursor.execute("""
        SELECT codeCours, nomCours, faculte FROM Cours
        WHERE nomCours LIKE %s OR codeCours LIKE %s ORDER BY nomCours
    """, (like_query, like_query))
    return [CourseInfo(r[0], r[1], r[2]) for r in cursor.fetchall()]

def insert_course(cursor, code: str, name: str, faculty: str) -> bool:
    try:
        cursor.execute("INSERT INTO Cours (codeCours, nomCours, faculte) VALUES (%s, %s, %s)", 
                       (code, name, faculty))
        return True
    except:
        return False # Echoue si le code cours existe deja

def get_summaries_by_course(cursor, course_id: str) -> List[SummaryInfo]:
    cursor.execute("""
        SELECT r.idResume, r.titre, COALESCE(r.description, ''), u.nomUtilisateur, r.datePublication,
               COALESCE(AVG(e.note), 0) as avg_rating, COUNT(e.note) as eval_count
        FROM Resume r
        JOIN Utilisateur u ON r.idUtilisateur = u.idUtilisateur
        LEFT JOIN Evalue e ON r.idResume = e.idResume
        WHERE r.codeCours = %s
        GROUP BY r.idResume, u.nomUtilisateur
        ORDER BY avg_rating DESC
    """, (course_id,))
    return [SummaryInfo(r[0], r[1], r[2], r[3], str(r[4]), float(r[5]), r[6]) for r in cursor.fetchall()]

def insert_summary(cursor, course_id: str, user_id: int, title: str, content: str, academic_year: str):
    """Insère un résumé en incluant l année académique choisie par l utilisateur."""
    cursor.execute("""
        INSERT INTO Resume (titre, description, datePublication, version, visibilite, idUtilisateur, codeCours, codeAnnee)
        VALUES (%s, %s, CURRENT_DATE(), 1, 'publique', %s, %s, %s)
    """, (title, content, user_id, course_id, academic_year))

def check_already_evaluated(cursor, summary_id: int, user_id: int) -> bool:
    cursor.execute("SELECT 1 FROM Evalue WHERE idResume = %s AND idUtilisateur = %s", (summary_id, user_id))
    return cursor.fetchone() is not None

def insert_evaluation(cursor, summary_id: int, user_id: int, rating: int, comment: str):
    cursor.execute("""
        INSERT INTO Evalue (idUtilisateur, idResume, note, commentaire, dateEvaluation)
        VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
    """, (user_id, summary_id, rating, comment))

def award_points(cursor, user_id: int, amount: int, reason: str):
    cursor.execute("UPDATE Utilisateur SET nombrePoints = nombrePoints + %s WHERE idUtilisateur = %s", (amount, user_id))
    cursor.execute("INSERT INTO TransactionPoints (montantPoints, natureTransaction, motif, idUtilisateur) VALUES (%s, 'gain', %s, %s)", (amount, reason, user_id))

def get_academic_years(cursor) -> List[str]:
    """Récupère la liste des années académiques existantes en base."""
    cursor.execute("SELECT codeAnnee FROM AnneeAcademique ORDER BY codeAnnee DESC")
    return [row[0] for row in cursor.fetchall()]
