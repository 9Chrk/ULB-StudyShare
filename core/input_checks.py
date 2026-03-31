"""Validation des entrées utilisateur pour l'authentification."""

import re

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
