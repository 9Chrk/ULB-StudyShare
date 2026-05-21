"""Validation des entrées utilisateur pour l'authentification."""

from core.constants import (
    USERNAME_MAX_LENGTH,
    PASSWORD_MAX_LENGTH,
    EMAIL_MAX_LENGTH,
    EMAIL_REGEX,
)


def validate_login_input(username: str, password: str) -> tuple[bool, str]:
    # Les champs ne peuvent pas être vides
    if is_blank(username) or is_blank(password):
        return False, "Username and password are required."

    # data cleanup
    username = username.strip()
    password = password.strip()

    # Les champs ne peuvent pas dépasser les longueurs maximales
    test_cases = [
        (username, USERNAME_MAX_LENGTH, "Username"),
        (password, PASSWORD_MAX_LENGTH, "Password"),
    ]

    # Validation de la longueur de chaque champ
    for value, max_length, field_name in test_cases:
        if not is_valid_length(value, max_length):
            return False, message_length_exceeded(field_name, max_length)

    return True, "Validation successful."


def validate_registration_input(
    username: str, password: str, email: str
) -> tuple[bool, str]:
    # Les champs ne peuvent pas être vides
    if is_blank(email):
        return False, "Email is required."

    # Réutilise la logique de validation de connexion pour username/password
    is_valid_login, login_message = validate_login_input(username, password)
    if not is_valid_login:
        return False, login_message

    # data cleanup
    email = email.strip()

    # Validation de la longueur uniquement pour l'email (username/password déjà vérifiés)
    if not is_valid_length(email, EMAIL_MAX_LENGTH):
        return False, message_length_exceeded("Email", EMAIL_MAX_LENGTH)

    # Le format de l'email doit être valide: <>@<>.<>
    if not is_valid_email(email):
        return False, "Invalid email format."

    return True, "Validation successful."


# ---------- FONCTIONS UTILITAIRES DE VALIDATION ----------


def is_blank(value: str) -> bool:
    """Renvoie True si la chaîne est vide ou ne contient que des espaces."""
    return not value or not value.strip()


def is_valid_email(email: str) -> bool:
    """Vérifie si l'email correspond au format attendu."""
    return EMAIL_REGEX.match(email) is not None


def is_valid_length(value: str, max_length: int) -> bool:
    """Vérifie si la chaîne ne dépasse pas la longueur maximale."""
    return len(value.strip()) <= max_length


def message_length_exceeded(field_name: str, max_length: int) -> str:
    """Génère un message d'erreur pour les champs dépassant la longueur maximale."""
    return f"{field_name} cannot exceed {max_length} characters."
