"""Validation des entrées utilisateurs pour l'authentification."""

from core.constants import (
    USERNAME_MAX_LENGTH,
    PASSWORD_MAX_LENGTH,
    EMAIL_MAX_LENGTH,
    EMAIL_REGEX,
)


def validate_login_input(username: str, password: str) -> tuple[bool, str]:
    """Valide les identifiants de connexion et renvoie un message explicite."""
    # Les champs ne peuvent pas être vides
    if _is_blank(username) or _is_blank(password):
        return False, "Le nom d'utilisateur et le mot de passe sont obligatoires."

    # nettoyage des données
    username = username.strip()
    password = password.strip()

    # Les champs ne peuvent pas dépasser les longueurs maximales
    test_cases = [
        (username, USERNAME_MAX_LENGTH, "Nom d'utilisateur"),
        (password, PASSWORD_MAX_LENGTH, "Mot de passe"),
    ]

    # Validation de la longueur de chaque champ
    for value, max_length, field_name in test_cases:
        if not _is_valid_length(value, max_length):
            return False, _message_length_exceeded(field_name, max_length)

    return True, "Validation réussie."


def validate_registration_input(
    username: str, password: str, email: str
) -> tuple[bool, str]:
    """Valide les données d'inscription en réutilisant les règles de connexion."""
    # Les champs ne peuvent pas être vides
    if _is_blank(email):
        return False, "L'e-mail est obligatoire."

    # Réutilise la logique de validation de connexion pour username/password
    is_valid_login, login_message = validate_login_input(username, password)
    if not is_valid_login:
        return False, login_message

    # nettoyage des données
    email = email.strip()

    # Validation de la longueur uniquement pour l'email (username/password déjà vérifiés)
    if not _is_valid_length(email, EMAIL_MAX_LENGTH):
        return False, _message_length_exceeded("E-mail", EMAIL_MAX_LENGTH)

    # Le format de l'email doit être valide: <>@<>.<>
    if not _is_valid_email(email):
        return False, "Le format de l'e-mail est invalide."

    return True, "Validation réussie."


# --------------------------------------------------------
# Méthodes de validation internes
# --------------------------------------------------------


def _is_blank(value: str) -> bool:
    """Renvoie True si la chaîne est vide ou ne contient que des espaces."""
    return not value or not value.strip()


def _is_valid_email(email: str) -> bool:
    """Vérifie si l'email correspond au format attendu."""
    return EMAIL_REGEX.match(email) is not None


def _is_valid_length(value: str, max_length: int) -> bool:
    """Vérifie si la chaîne ne dépasse pas la longueur maximale."""
    return len(value.strip()) <= max_length


def _message_length_exceeded(field_name: str, max_length: int) -> str:
    """Génère un message d'erreur pour les champs dépassant la longueur maximale."""
    return f"{field_name} ne peut pas dépasser {max_length} caractères."
