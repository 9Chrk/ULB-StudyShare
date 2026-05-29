"""Orchestrateur d'import des données fichiers vers la base SQL.

Ce module centralise le pipeline complet :
1) lecture CSV/XML/JSON,
2) reset des tables cible,
3) insertion par domaine métier dans un ordre compatible FK/triggers.
"""

from core.db.manager import DBManager
from core.importers.courses import import_course_year_links, import_courses
from core.importers.evaluations import import_evaluations
from core.importers.objects import import_objects
from core.importers.resumes import import_resumes
from core.importers.users import apply_active_objects, import_possessions, import_users
from core.parsers.csv_parser import csv_to_dict
from core.parsers.json_parser import json_to_dict
from core.parsers.xml_parser import xml_to_dict


DEFAULT_YEAR_CODE = "2025"
DEFAULT_YEAR_LABEL = "2025-2026"
RESET_TABLES = [
    "Evalue",
    "Possede",
    "Resume",
    "TransactionPoints",
    "EstDonnePendant",
    "Utilisateur",
    "Badge",
    "Titre",
    "ThemeProfil",
    "ObjetCosmetique",
    "Cours",
    "AnneeAcademique",
]


def _reset_import_tables(cursor) -> None:
    """Vide les tables importées pour repartir d'un état propre.

    L'ordre est explicite via 'RESET_TABLES'. Les contraintes FK sont
    désactivées temporairement pour permettre le 'TRUNCATE' en chaine.
    """
    # Les FK doivent être coupées temporairement sinon les TRUNCATE échouent.
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    try:
        for table_name in RESET_TABLES:
            cursor.execute(f"TRUNCATE TABLE {table_name}")
    finally:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")


def import_data(
    courses_path: str = "data/cours.csv",
    objects_path: str = "data/recompenses.xml",
    users_path: str = "data/utilisateurs",
    evaluations_path: str = "data/commentaires.json",
) -> dict[str, int]:
    """Importe les fichiers 'data' dans SQL et retourne les statistiques.

    Returns:
        dict[str, int]: compteurs d'insertion et de lignes ignorées.
    """
    stats = {
        "courses": 0,
        "course_year_links": 0,
        "objects": 0,
        "users": 0,
        "resumes": 0,
        "possessions": 0,
        "active_objects": 0,
        "evaluations": 0,
        "transactions": 0,
        "skipped": 0,
    }

    # On parse chaque source une seule fois pour éviter de relire les fichiers plusieurs fois.
    courses = csv_to_dict(courses_path)
    objects = xml_to_dict(objects_path)
    users = xml_to_dict(users_path)
    evaluations = json_to_dict(evaluations_path)

    with DBManager() as cursor:
        # On repart toujours d'une base vide pour garantir un import déterministe.
        _reset_import_tables(cursor)

        # Import des références (cours + année) avant les entités dépendantes.
        course_codes = import_courses(cursor, courses, stats)
        import_course_year_links(
            cursor, course_codes, DEFAULT_YEAR_CODE, DEFAULT_YEAR_LABEL, stats
        )

        # Les objets et les utilisateurs servent d'ancres pour les relations suivantes.
        object_map = import_objects(cursor, objects, stats)
        user_map = import_users(cursor, users, stats)

        # Les résumés, possessions, activations et évaluations dépendent des maps précédentes.
        resume_map = import_resumes(
            cursor, users, user_map, course_codes, DEFAULT_YEAR_CODE, stats
        )
        import_possessions(cursor, users, user_map, object_map, stats)
        apply_active_objects(cursor, users, user_map, object_map, stats)

        import_evaluations(cursor, evaluations, user_map, resume_map, stats)

    return stats
