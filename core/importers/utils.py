"""Utilitaires simples pour normaliser les données d'import."""

from datetime import date, datetime


def clean_text(value: object) -> str:
    """Convertit une valeur en texte propre (None -> '')."""
    return str(value or "").strip()


def as_list(value: object) -> list:
    """Force une valeur XML/JSON en liste pour itérer simplement."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def to_int(value: object, default: int) -> int:
    """Convertit une valeur en entier, sinon retourne default."""
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def bounded_int(value: object, default: int, minimum: int, maximum: int | None = None) -> int:
    """Convertit en entier en respectant un intervalle de valeurs autorisé."""
    number = to_int(value, default)

    if number < minimum:
        return default

    if maximum is not None and number > maximum:
        return default

    return number


def sql_datetime_or_now(value: object) -> str:
    """Retourne un datetime SQL valide, sinon l'instant courant."""
    text = clean_text(value)

    if not text:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if len(text) == 10:
        try:
            return date.fromisoformat(text).strftime("%Y-%m-%d 00:00:00")
        except ValueError:
            pass

    try:
        return datetime.fromisoformat(text).strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
