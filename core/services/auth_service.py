"""Services d'authentification (accès DB + règles métier de base)."""

import mysql.connector
from typing import Optional, Tuple

from core.db.manager import DBManager
from core.auth.validators import validate_login_input, validate_registration_input
from core.repository.user_repository import get_user_id_with_credentials, username_or_email_exists, insert_user


def check(username: str, password: str) -> Tuple[bool, str, Optional[int]]:
    """Vérifie les identifiants de connexion fournis par l'utilisateur."""
    # 1) Validation côté applicatif (longueur, champs vides, etc.)
    is_valid, error = validate_login_input(username, password)
    
    if not is_valid:
        return False, error, None

    # 2) Récupération de l'ID utilisateur en base
    with DBManager() as cursor:
        user_id = get_user_id_with_credentials(cursor, username.strip(), password)

    # 3) Aucun enregistrement trouvé : on renvoie un message d'erreur générique
    if not user_id:
        return False, "Incorrect username or password.", None

    return True, "Success", user_id


def add(username: str, password: str, email: str) -> Tuple[bool, str]:
    """Crée un nouvel utilisateur si les données sont valides et disponibles."""
    # 1) Validation des données d'inscription
    is_valid, error = validate_registration_input(username, password, email)
    
    if not is_valid:
        return False, error

    username = username.strip()
    email = email.strip()

    try:
        # 2) Vérifier que le nom d'utilisateur ou l'email ne sont pas déjà utilisés
        with DBManager() as cursor:
            user_or_email_exists = username_or_email_exists(cursor, username, email)

            if user_or_email_exists:
                return False, "Username or email already exists."

            # 3) Insérer le nouvel utilisateur
            insert_user(cursor, username, email, password)
            
        return True, "Account created successfully."
    
    except mysql.connector.Error:
        return False, "Unable to create the account at the moment."
