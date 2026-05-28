"""Point d'entrée principal: GUI toujours, import optionnel avec --init."""

import sys
import mysql.connector

from core.db.init import execute_sql_script
from core.importers.service import import_data
from gui.app import run


def print_import_stats(stats: dict[str, int]) -> None:
    """Affiche les compteurs issus de l'import en mode console."""
    print("Import terminé.\n")
    print("-------- Statistiques --------")

    lines = [
        ("Cours", stats["courses"]),
        ("Liens cours/année", stats["course_year_links"]),
        ("Objets", stats["objects"]),
        ("Utilisateurs", stats["users"]),
        ("Résumés", stats["resumes"]),
        ("Objets possédés", stats["possessions"]),
        ("Objets actifs appliqués", stats["active_objects"]),
        ("Évaluations", stats["evaluations"]),
        ("Lignes ignorées", stats["skipped"]),
    ]

    width = max(len(label) for label, _ in lines)
    for label, count in lines:
        print(f"- {label:<{width}} : {count}")

    print("------------------------------\n")


def run_import_mode() -> None:
    """Lance l'import des données puis affiche le résumé des statistiques."""
    stats = import_data()
    print_import_stats(stats)


def main(argv: list[str] | None = None) -> None:
    """Point d'entrée CLI: initialise la base, importe si demandé, puis lance la GUI."""
    args = argv if argv is not None else sys.argv
    options = [arg.strip().lower() for arg in args[1:]]

    init_requested = "--init" in options
    unknown_options = [option for option in options if option != "--init"]

    if unknown_options:
        print("Usage: python3 main.py [--init]")
        return

    execute_sql_script("schema.sql")

    if init_requested:
        try:
            run_import_mode()
        except mysql.connector.Error as error:
            print("Erreur MySQL pendant l'import:", error)

    run()


if __name__ == "__main__":
    main()
