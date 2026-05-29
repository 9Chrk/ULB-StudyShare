"""Import des cours et de leur rattachement à une année académique."""

import mysql.connector

from core.importers.utils import clean_text


def import_courses(
    cursor, courses: list[dict[str, str]], stats: dict[str, int]
) -> set[str]:
    """Insère les cours CSV valides.

    Args:
        cursor: curseur SQL actif.
        courses: lignes parsées du fichier 'cours.csv'.
        stats: accumulateur de compteurs d'import.

    Returns:
        set[str]: codes de cours effectivement insérés.
    """
    course_codes: set[str] = set()

    for row in courses:
        code = clean_text(row.get("code_cours"))
        name = clean_text(row.get("nom"))
        faculty = clean_text(row.get("faculte"))

        # On ignore les lignes incomplètes avant insert SQL.
        if not code or not name or not faculty:
            stats["skipped"] += 1
            continue

        try:
            cursor.execute(
                """
                INSERT INTO Cours (codeCours, nomCours, faculte)
                VALUES (%s, %s, %s)
                """,
                (code, name, faculty),
            )
            course_codes.add(code)
            stats["courses"] += 1
        except mysql.connector.Error:
            stats["skipped"] += 1

    return course_codes


def import_course_year_links(
    cursor,
    course_codes: set[str],
    year_code: str,
    year_label: str,
    stats: dict[str, int],
) -> None:
    """Crée l'année académique cible puis associe tous les cours importés.

    Cette fonction se base sur les 'course_codes' retournés par
    'import_courses' pour remplir 'EstDonnePendant'.
    """
    try:
        cursor.execute(
            """
            INSERT INTO AnneeAcademique (codeAnnee, libelle)
            VALUES (%s, %s)
            """,
            (year_code, year_label),
        )
    except mysql.connector.Error:
        stats["skipped"] += 1
        return

    for code in course_codes:
        try:
            cursor.execute(
                "INSERT INTO EstDonnePendant (codeCours, codeAnnee) VALUES (%s, %s)",
                (code, year_code),
            )
            stats["course_year_links"] += 1
        except mysql.connector.Error:
            stats["skipped"] += 1
