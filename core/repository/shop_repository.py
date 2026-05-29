"""Requêtes SQL liées à la boutique."""

from typing import List, Optional

from core.models.shop import ShopItem
from core.models.shop import ShopUserState


def get_catalogue(cursor) -> List[ShopItem]:
    """Renvoie le catalogue complet avec la catégorie de chaque objet."""
    # Les LEFT JOIN permettent d'identifier le sous-type sans requête supplémentaire.
    cursor.execute(
        """
        SELECT
            oc.idObjet,
            oc.nomObjet,
            oc.description,
            oc.prixPoints,
            CASE
                WHEN b.idObjet IS NOT NULL THEN 'badge'
                WHEN t.idObjet IS NOT NULL THEN 'titre'
                WHEN tp.idObjet IS NOT NULL THEN 'theme'
                ELSE 'autre'
            END AS typeObjet
        FROM ObjetCosmetique oc
        LEFT JOIN Badge b ON b.idObjet = oc.idObjet
        LEFT JOIN Titre t ON t.idObjet = oc.idObjet
        LEFT JOIN ThemeProfil tp ON tp.idObjet = oc.idObjet
        ORDER BY oc.prixPoints ASC, oc.nomObjet ASC
        """
    )
    rows = cursor.fetchall()
    return [
        ShopItem(
            item_id=row[0],
            name=row[1],
            description=row[2],
            price_points=row[3],
            item_type=row[4],
        )
        for row in rows
    ]


def get_owned_item_ids(cursor, user_id: int) -> List[int]:
    """Renvoie les IDs des objets possédés par l'utilisateur."""
    cursor.execute(
        "SELECT idObjet FROM Possede WHERE idUtilisateur = %s",
        (user_id,),
    )
    return [row[0] for row in cursor.fetchall()]


def get_user_shop_state(cursor, user_id: int) -> Optional[ShopUserState]:
    """Renvoie les points et objets actifs d'un utilisateur."""
    cursor.execute(
        """
        SELECT nombrePoints, idBadgeActif, idTitreActif, idThemeActif
        FROM Utilisateur
        WHERE idUtilisateur = %s
        """,
        (user_id,),
    )
    row = cursor.fetchone()
    if row is None:
        return None
    return ShopUserState(
        points=row[0],
        active_badge_id=row[1],
        active_title_id=row[2],
        active_theme_id=row[3],
    )


def get_item_by_id(cursor, item_id: int) -> Optional[ShopItem]:
    """Renvoie un objet du catalogue par son ID."""
    # Même stratégie que get_catalogue(): une seule requête pour récupérer le sous-type.
    cursor.execute(
        """
        SELECT
            oc.idObjet,
            oc.nomObjet,
            oc.description,
            oc.prixPoints,
            CASE
                WHEN b.idObjet IS NOT NULL THEN 'badge'
                WHEN t.idObjet IS NOT NULL THEN 'titre'
                WHEN tp.idObjet IS NOT NULL THEN 'theme'
                ELSE 'autre'
            END AS typeObjet
        FROM ObjetCosmetique oc
        LEFT JOIN Badge b ON b.idObjet = oc.idObjet
        LEFT JOIN Titre t ON t.idObjet = oc.idObjet
        LEFT JOIN ThemeProfil tp ON tp.idObjet = oc.idObjet
        WHERE oc.idObjet = %s
        """,
        (item_id,),
    )
    row = cursor.fetchone()
    if row is None:
        return None
    return ShopItem(
        item_id=row[0],
        name=row[1],
        description=row[2],
        price_points=row[3],
        item_type=row[4],
    )


def is_item_owned(cursor, user_id: int, item_id: int) -> bool:
    """Vérifie si l'utilisateur possède déjà l'objet."""
    cursor.execute(
        "SELECT 1 FROM Possede WHERE idUtilisateur = %s AND idObjet = %s",
        (user_id, item_id),
    )
    return cursor.fetchone() is not None


def add_owned_item(cursor, user_id: int, item_id: int) -> None:
    """Ajoute un objet à l'inventaire de l'utilisateur."""
    cursor.execute(
        "INSERT INTO Possede (idUtilisateur, idObjet) VALUES (%s, %s)",
        (user_id, item_id),
    )


def spend_user_points(cursor, user_id: int, amount: int) -> None:
    """Déduit des points du solde de l'utilisateur."""
    cursor.execute(
        """
        UPDATE Utilisateur
        SET nombrePoints = nombrePoints - %s
        WHERE idUtilisateur = %s
        """,
        (amount, user_id),
    )


def create_spend_transaction(cursor, user_id: int, amount: int, reason: str) -> None:
    """Historise la dépense de points liée à un achat boutique."""
    cursor.execute(
        """
        INSERT INTO TransactionPoints (montantPoints, natureTransaction, motif, idUtilisateur)
        VALUES (%s, 'depense', %s, %s)
        """,
        (amount, reason, user_id),
    )


def activate_item(cursor, user_id: int, item_id: int, item_type: str) -> bool:
    """Active un objet possédé selon son type (badge, titre, thème)."""
    if item_type == "badge":
        # Chaque type met à jour une colonne différente dans Utilisateur.
        cursor.execute(
            "UPDATE Utilisateur SET idBadgeActif = %s WHERE idUtilisateur = %s",
            (item_id, user_id),
        )
        return True

    if item_type == "titre":
        # Le titre actif suit exactement la même logique que le badge.
        cursor.execute(
            "UPDATE Utilisateur SET idTitreActif = %s WHERE idUtilisateur = %s",
            (item_id, user_id),
        )
        return True

    if item_type == "theme":
        # Les thèmes sont stockés dans leur propre colonne d'activation.
        cursor.execute(
            "UPDATE Utilisateur SET idThemeActif = %s WHERE idUtilisateur = %s",
            (item_id, user_id),
        )
        return True

    return False
