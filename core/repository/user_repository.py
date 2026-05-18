"""Requêtes SQL liées à l'entité Utilisateur."""
from typing import Optional, List, Tuple
from core.models.user import UserInfo


def get_user_id_with_credentials(cursor, username: str, password: str) -> Optional[int]:
    cursor.execute(
        "SELECT idUtilisateur FROM Utilisateur WHERE nomUtilisateur = %s AND motDePasse = %s",
        (username, password),
    )
    row = cursor.fetchone()
    return row[0] if row is not None else None


def username_or_email_exists(cursor, username: str, email: str) -> bool:
    cursor.execute(
        "SELECT 1 FROM Utilisateur WHERE nomUtilisateur = %s OR email = %s",
        (username, email),
    )
    return cursor.fetchone() is not None


def insert_user(cursor, username: str, email: str, password: str) -> None:
    cursor.execute(
        """
        INSERT INTO Utilisateur (nomUtilisateur, email, motDePasse, dateInscription, niveau, nombrePoints)
        VALUES (%s, %s, %s, CURRENT_DATE(), 1, 0)
        """,
        (username, email, password),
    )


def get_user_info(cursor, user_id: int) -> Optional[UserInfo]:
    cursor.execute(
        "SELECT nomUtilisateur, email, dateInscription, niveau, nombrePoints FROM Utilisateur WHERE idUtilisateur = %s",
        (user_id,),
    )
    row = cursor.fetchone()
    if row is None:
        return None
    return UserInfo(
        username=row[0],
        email=row[1],
        registration_date=row[2],
        level=row[3],
        points=row[4],
    )


def get_active_title(cursor, user_id: int) -> Optional[str]:
    cursor.execute(
        """
        SELECT oc.nomObjet
        FROM Utilisateur u
        JOIN ObjetCosmetique oc ON u.idTitreActif = oc.idObjet
        WHERE u.idUtilisateur = %s AND u.idTitreActif IS NOT NULL
        """,
        (user_id,)
    )
    row = cursor.fetchone()
    return row[0] if row else None


def get_recent_activity(cursor, user_id: int) -> List[Tuple]:
    cursor.execute(
        """
        SELECT 'Published' AS type, r.titre, r.datePublication AS date
        FROM Resume r
        WHERE r.idUtilisateur = %s
        UNION ALL
        SELECT 'Evaluated' AS type, r.titre, e.dateEvaluation AS date
        FROM Evalue e
        JOIN Resume r ON e.idResume = r.idResume
        WHERE e.idUtilisateur = %s
        ORDER BY date DESC
        LIMIT 5
        """,
        (user_id, user_id)
    )
    return cursor.fetchall()
