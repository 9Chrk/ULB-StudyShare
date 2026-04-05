"""Import des objets cosmétiques."""

import mysql.connector

from core.importers.utils import bounded_int, clean_text


def import_objects(cursor, objects: list[dict], stats: dict[str, int]) -> dict[str, tuple[int, str]]:
    """Insère les objets cosmétiques et renvoie un index nom -> (id, type)."""
    object_map: dict[str, tuple[int, str]] = {}
    subtype_tables = {
        "badge": "Badge",
        "titre": "Titre",
        "theme": "ThemeProfil",
    }

    for row in objects:
        object_id = bounded_int(row.get("id"), default=0, minimum=1)
        name = clean_text(row.get("nom"))
        object_type = clean_text(row.get("type")).lower()
        description = clean_text(row.get("description")) or "Objet importé"
        points = bounded_int(row.get("prix"), default=1, minimum=1)

        if not object_id or not name or object_type not in {"badge", "titre", "theme", "cosmetique"}:
            stats["skipped"] += 1
            continue

        try:
            cursor.execute(
                """
                INSERT INTO ObjetCosmetique (idObjet, nomObjet, description, prixPoints)
                VALUES (%s, %s, %s, %s)
                """,
                (object_id, name, description, points),
            )
            object_map[name] = (object_id, object_type)

            subtype_table = subtype_tables.get(object_type)
            if subtype_table:
                cursor.execute(
                    f"INSERT IGNORE INTO {subtype_table} (idObjet) VALUES (%s)",
                    (object_id,),
                )

            stats["objects"] += 1
        except mysql.connector.Error:
            stats["skipped"] += 1

    return object_map
