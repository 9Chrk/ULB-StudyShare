import re

import mysql.connector

from core.db_manager import DBManager

_USERNAME_MAX_LENGTH = 50
_EMAIL_MAX_LENGTH = 255
_PASSWORD_MAX_LENGTH = 255
_EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _is_blank(value: str) -> bool:
    return not value or not value.strip()


def validate_login_input(username: str, password: str) -> tuple[bool, str]:
    if _is_blank(username) or _is_blank(password):
        return False, "Le nom d'utilisateur et le mot de passe sont obligatoires."

    if len(username.strip()) > _USERNAME_MAX_LENGTH:
        return False, f"Le nom d'utilisateur ne peut pas dépasser {_USERNAME_MAX_LENGTH} caractères."

    if len(password) > _PASSWORD_MAX_LENGTH:
        return False, f"Le mot de passe ne peut pas dépasser {_PASSWORD_MAX_LENGTH} caractères."

    return True, ""


def validate_registration_input(username: str, password: str, email: str) -> tuple[bool, str]:
    if _is_blank(username) or _is_blank(email) or _is_blank(password):
        return False, "Tous les champs sont obligatoires."

    username = username.strip()
    email = email.strip()

    if len(username) > _USERNAME_MAX_LENGTH:
        return False, f"Le nom d'utilisateur ne peut pas dépasser {_USERNAME_MAX_LENGTH} caractères."

    if len(email) > _EMAIL_MAX_LENGTH:
        return False, f"L'email ne peut pas dépasser {_EMAIL_MAX_LENGTH} caractères."

    if len(password) > _PASSWORD_MAX_LENGTH:
        return False, f"Le mot de passe ne peut pas dépasser {_PASSWORD_MAX_LENGTH} caractères."

    if not _EMAIL_REGEX.match(email):
        return False, "Le format de l'email est invalide."

    return True, ""


def check(username: str, password: str) -> tuple[bool, str]:
    is_valid, error = validate_login_input(username, password)
    if not is_valid:
        return False, error

    with DBManager() as cursor:
        cursor.execute(
            "SELECT 1 FROM Utilisateur WHERE nomUtilisateur = %s AND motDePasse = %s",
            (username.strip(), password)
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
                (username, email)
            )

            if cursor.fetchone():
                return False, "Le nom d'utilisateur ou l'email existe déjà."

            cursor.execute(
                """
                INSERT INTO Utilisateur (nomUtilisateur, email, motDePasse, dateInscription, niveau, nombrePoints)
                VALUES (%s, %s, %s, CURRENT_DATE(), 1, 0)
                """,
                (username, email, password)
            )

        return True, ""
    except mysql.connector.Error:
        return False, "Impossible de créer le compte pour le moment."
