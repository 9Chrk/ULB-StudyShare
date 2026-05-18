"""Requêtes SQL liées à la boutique."""
from typing import List, Tuple

def get_catalogue(cursor) -> List[Tuple]:
    """Renvoie tous les objets cosmétiques."""
    cursor.execute(
        """
        SELECT idObjet, nomObjet, description, prixPoints
        FROM ObjetCosmetique
        ORDER BY prixPoints ASC
        """
    )
    return cursor.fetchall()



def get_owned_item_ids(cursor, user_id: int) -> List[int]:
    """Renvoie les IDs des objets possédés par l'utilisateur."""
    cursor.execute(
        "SELECT idObjet FROM Possede WHERE idUtilisateur = %s",
        (user_id,)
    )
    return [row[0] for row in cursor.fetchall()]
