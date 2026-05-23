"""Logique métier pour 'My Library'"""

from typing import List, Tuple
from core.db.manager import DBManager
from core.repository import my_library_repository as repo

class LibraryService:
    def get_my_summaries(self, user_id: int) -> List[Tuple]:
        """Récupère l historique des résumés publié par l utilisateur connecté."""
        with DBManager() as cursor:
            return repo.get_user_summaries(cursor, user_id)

    def update_my_summary(self, summary_id: int, user_id: int, title: str, content: str) -> Tuple[bool, str]:
        """Modifie le titre ou la description d un résumé possédé."""
        if not title.strip() or not content.strip():
            return False, "Le titre et la description ne peuvent pas être vides."
            
        with DBManager() as cursor:
            success = repo.update_user_summary(cursor, summary_id, user_id, title.strip(), content.strip())
            
        if success:
            return True, "Votre résumé a bien été modifié."
        # on peut pas modif un résumé qui nous appartient pas
        return False, "Erreur lors de la modification (Vérifiez vos droits)."

    def delete_my_summary(self, summary_id: int, user_id: int) -> Tuple[bool, str]:
        """Supprime un résumé."""
        with DBManager() as cursor:
            success = repo.delete_user_summary(cursor, summary_id, user_id)
            
        if success:
            return True, "Résumé supprimé définitivement."
        # on peut pas modif un résumé qui nous appartient pas
        return False, "Impossible de supprimer ce résumé."

    def get_my_evaluations(self, user_id: int) -> List[Tuple]:
        """Récupère les avis laisser par les autres sur tes résumés."""
        with DBManager() as cursor:
            return repo.get_evaluations_received(cursor, user_id)
