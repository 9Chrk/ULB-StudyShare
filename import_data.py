"""Script d'import des données JSON/CSV/XML vers la base MySQL."""

import mysql.connector

from core.db.init import execute_sql_script
from core.importers import import_data


def print_stats(stats: dict[str, int]) -> None:
    print("Import terminé.")
    print("- Cours importés:", stats["courses"])
    print("- Liens cours/année:", stats["course_year_links"])
    print("- Objets importés:", stats["objects"])
    print("- Utilisateurs importés:", stats["users"])
    print("- Résumés importés:", stats["resumes"])
    print("- Objets possédés importés:", stats["possessions"])
    print("- Objets actifs appliqués:", stats["active_objects"])
    print("- Évaluations importées:", stats["evaluations"])
    print("- Lignes ignorées:", stats["skipped"])


def main() -> None:
    try:
        execute_sql_script("schema.sql")
        stats = import_data()
        print_stats(stats)
    except mysql.connector.Error as error:
        print("Erreur MySQL pendant l'import:", error)


if __name__ == "__main__":
    main()
