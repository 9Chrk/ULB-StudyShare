"""Services d'authentification (accès DB + règles métier de base)."""

import mysql.connector
from typing import Optional, Tuple

from core.db.manager import DBManager
from core.auth.validators import validate_login_input, validate_registration_input
from core.repository.user_repository import (
    get_user_id_with_credentials,
    username_or_email_exists,
    insert_user,
)


def check(username: str, password: str) -> Tuple[bool, str, Optional[int]]:
    """Vérifie les identifiants de connexion fournis par l'utilisateur."""
    # 1) Validation côté applicatif (longueur, champs vides, etc.)
    is_valid, error = validate_login_input(username, password)

    if not is_valid:
        return False, error, None

    try:
        # 2) Récupération de l'ID utilisateur en base
        with DBManager() as cursor:
            user_id = get_user_id_with_credentials(cursor, username.strip(), password)

    except mysql.connector.Error:
        return False, "Connexion à la base de données impossible.", None

    # 3) Aucun enregistrement trouvé : on renvoie un message d'erreur générique
    if not user_id:
        return False, "Nom d'utilisateur ou mot de passe incorrect.", None

    return True, "Connexion réussie.", user_id


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
                return False, "Ce nom d'utilisateur ou cet e-mail existe déjà."

            # 3) Insérer le nouvel utilisateur
            insert_user(cursor, username, email, password)

        return True, "Compte créé avec succès."

    except mysql.connector.Error:
        return False, "Impossible de créer le compte pour le moment."
