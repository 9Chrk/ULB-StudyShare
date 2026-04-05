"""Requêtes SQL liées à l'entité Utilisateur."""

from typing import Optional

from core.models.user import UserInfo


def get_user_id_with_credentials(cursor, username: str, password: str) -> Optional[int]:
    """Renvoie l'ID d'un utilisateur, ou None."""
    cursor.execute(
        "SELECT idUtilisateur FROM Utilisateur WHERE nomUtilisateur = %s AND motDePasse = %s",
        (username, password),
    )
    row = cursor.fetchone()
    return row[0] if row is not None else None


def username_or_email_exists(cursor, username: str, email: str) -> bool:
    """Renvoie True si le nom d'utilisateur ou l'email existe déjà."""
    cursor.execute(
        "SELECT 1 FROM Utilisateur WHERE nomUtilisateur = %s OR email = %s",
        (username, email),
    )
    return cursor.fetchone() is not None


def insert_user(cursor, username: str, email: str, password: str) -> None:
    """Insère un nouvel utilisateur dans la base."""
    cursor.execute(
        """
        INSERT INTO Utilisateur (nomUtilisateur, email, motDePasse, dateInscription, niveau, nombrePoints)
        VALUES (%s, %s, %s, CURRENT_DATE(), 1, 0)
        """,
        (username, email, password),
    )


def get_user_info(cursor, user_id: int) -> Optional[UserInfo]:
    """Renvoie les informations de l'utilisateur, ou None si absent."""
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
