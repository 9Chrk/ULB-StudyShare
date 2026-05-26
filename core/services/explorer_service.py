"""Logique métier pour l'Explorer"""

from typing import List, Tuple, Optional
from core.db.manager import DBManager
from core.repository import explorer_repository as repo
from core.repository.explorer_repository import CourseInfo, SummaryInfo

class ExplorerService:
    def get_courses(self, search_query: Optional[str] = None) -> List[CourseInfo]:
        with DBManager() as cursor:
            if search_query and search_query.strip():
                return repo.search_courses(cursor, search_query.strip())
            return repo.get_all_courses(cursor)

    def add_course(self, code: str, name: str, faculty: str) -> Tuple[bool, str]:
        if not code or not name: return False, "Code et Nom obligatoires."
        with DBManager() as cursor:
            if repo.insert_course(cursor, code.strip().upper(), name.strip(), faculty.strip()):
                return True, "Cours ajouté avec succès."
            return False, "Ce code de cours existe déjà."

    def get_summaries_for_course(self, course_id: str) -> List[SummaryInfo]:
        with DBManager() as cursor:
            return repo.get_summaries_by_course(cursor, course_id)

    def publish_summary(self, course_id: str, user_id: int, title: str, content: str, academic_year: str) -> Tuple[bool, str]:
        if not title.strip() or not content.strip() or not academic_year.strip(): 
            return False, "Tous les champs sont obligatoires."
            
        with DBManager() as cursor:
            repo.insert_summary(cursor, course_id, user_id, title.strip(), content.strip(), academic_year.strip())
            repo.award_points(cursor, user_id, 10, "Publication résumé")
        
            
        return True, "Résumé publié ! +10 points."

    def evaluate_summary(self, summary_id: int, user_id: int, rating: int, comment: str) -> Tuple[bool, str]:
        if not (1 <= rating <= 5): return False, "Note invalide."
        with DBManager() as cursor:
            if repo.check_already_evaluated(cursor, summary_id, user_id):
                return False, "Déjà évalué."
            repo.insert_evaluation(cursor, summary_id, user_id, rating, comment.strip())
            repo.award_points(cursor, user_id, 2, "Évaluation résumé")
        return True, "Évalué ! +2 points."
    def get_academic_years(self) -> List[str]:
        with DBManager() as cursor:
            return repo.get_academic_years(cursor)
