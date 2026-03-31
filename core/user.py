from core import db_manager
from core.db_manager import DBManager


def check(username, password):
    with DBManager() as cursor:
        cursor.execute(
            "SELECT * FROM Utilisateur WHERE nomUtilisateur = %s AND motDePasse = %s",
            (username, password)
        )
        return cursor.fetchone() is not None


def add(username, password, email):
    with DBManager() as cursor:
        cursor.execute(
            "SELECT * FROM Utilisateur WHERE nomUtilisateur = %s OR email = %s",
            (username, email)
        )

        if cursor.fetchone():
            return False
        
        cursor.execute(
            """
            INSERT INTO Utilisateur (nomUtilisateur, email, motDePasse, dateInscription, niveau, nombrePoints)
            VALUES (%s, %s, %s, CURRENT_DATE(), 1, 0)
            """,
            (username, email, password)
        )
        return True
