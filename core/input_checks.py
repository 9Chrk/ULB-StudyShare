"""Validation des entrées utilisateur pour l'authentification."""

import re

############### CONSTANTES DE VALIDATION #################
USERNAME_MAX_LENGTH = 50
EMAIL_MAX_LENGTH = 255
PASSWORD_MAX_LENGTH = 255
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
##########################################################


def is_blank(value: str) -> bool:
    return not value or not value.strip()


def validate_login_input(username: str, password: str) -> tuple[bool, str]:
    # Les champs ne peuvent pas être vides
    if is_blank(username) or is_blank(password):
        return False, "Username and password are required."
    # Les champs ne peuvent pas dépasser les longueurs maximales
    if len(username.strip()) > USERNAME_MAX_LENGTH:
        return False, f"Username cannot exceed {USERNAME_MAX_LENGTH} characters."
    # idem
    if len(password) > PASSWORD_MAX_LENGTH:
        return False, f"Password cannot exceed {PASSWORD_MAX_LENGTH} characters."

    return True, ""


def validate_registration_input(username: str, password: str, email: str) -> tuple[bool, str]:
    # Les champs ne peuvent pas être vides
    if is_blank(username) or is_blank(email) or is_blank(password):
        return False, "Tous les champs sont obligatoires."

    username = username.strip()
    email = email.strip()

    # Les champs ne peuvent pas dépasser les longueurs maximales
    if len(username) > USERNAME_MAX_LENGTH:
        return False, f"Username cannot exceed {USERNAME_MAX_LENGTH} characters."

    if len(email) > EMAIL_MAX_LENGTH:
        return False, f"Email cannot exceed {EMAIL_MAX_LENGTH} characters."

    if len(password) > PASSWORD_MAX_LENGTH:
        return False, f"Password cannot exceed {PASSWORD_MAX_LENGTH} characters."

    # Le format de l'email doit être valide: <>@<>.<>
    if not EMAIL_REGEX.match(email):
        return False, "Invalid email format."

    return True, ""
