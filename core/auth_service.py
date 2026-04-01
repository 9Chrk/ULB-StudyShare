"""Services d'authentification (accès DB + règles métier de base)."""

import mysql.connector

from core.db_manager import DBManager
from core.input_checks import validate_login_input, validate_registration_input


def check(username: str, password: str) -> tuple[bool, str]:
    is_valid, error = validate_login_input(username, password)
    
    if not is_valid:
        return False, error

    with DBManager() as cursor:
        cursor.execute(
            "SELECT 1 FROM Utilisateur WHERE nomUtilisateur = %s AND motDePasse = %s",
            (username.strip(), password),
        )
        user_exists = cursor.fetchone() is not None

    if not user_exists:
        return False, "Nom d'utilisateur ou mot de passe incorrect."

    return True, ""


def add(username: str, password: str, email: str) -> tuple[bool, str]:
    is_valid, error = validate_registration_input(username, password, email)
    
    if not is_valid:
        return False, error

    username = username.strip()
    email = email.strip()

    try:
        with DBManager() as cursor:
            cursor.execute(
                "SELECT 1 FROM Utilisateur WHERE nomUtilisateur = %s OR email = %s",
                (username, email),
            )
            user_or_email_exists = cursor.fetchone() is not None

            if user_or_email_exists:
                return False, "Le nom d'utilisateur ou l'email existe déjà."

            cursor.execute(
                """
                INSERT INTO Utilisateur (nomUtilisateur, email, motDePasse, dateInscription, niveau, nombrePoints)
                VALUES (%s, %s, %s, CURRENT_DATE(), 1, 0)
                """,
                (username, email, password),
            )
        return True, ""
    
    except mysql.connector.Error:
        return False, "Impossible de créer le compte pour le moment."
