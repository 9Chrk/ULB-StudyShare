"""Import des utilisateurs, objets possédés et objets actifs."""

from datetime import date
import mysql.connector

from core.importers.utils import as_list, bounded_int, clean_text


def import_users(cursor, users: list[dict], stats: dict[str, int]) -> dict[str, int]:
    """Insère les utilisateurs et construit un index ``nom -> id``.

    L'import remplit un mot de passe factice (nom d'utilisateur) pour
    garantir une valeur non nulle lors de l'initialisation.
    """
    user_map: dict[str, int] = {}

    for user in users:
        user_id = bounded_int(user.get("id"), default=0, minimum=1)
        username = clean_text(user.get("nomUtilisateur"))
        email = clean_text(user.get("email"))

        # On ignore les enregistrements incomplets avant d'attaquer l'INSERT.
        if not user_id or not username or not email:
            stats["skipped"] += 1
            continue

        date_inscription = clean_text(user.get("dateInscription"))

        # La date d'inscription peut être absente ou invalide dans la source.
        try:
            date_inscription = date.fromisoformat(date_inscription).strftime("%Y-%m-%d")
        except ValueError:
            # Repli robuste pour éviter les erreurs SQL sur DATE NOT NULL.
            date_inscription = date.today().strftime("%Y-%m-%d")

        level = bounded_int(user.get("niveau"), default=1, minimum=1)
        points = bounded_int(user.get("points"), default=0, minimum=0)

        try:
            cursor.execute(
                """
                INSERT INTO Utilisateur (idUtilisateur, nomUtilisateur, email, motDePasse, dateInscription, niveau, nombrePoints)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (user_id, username, email, username, date_inscription, level, points),
            )

            user_map[username] = user_id
            stats["users"] += 1
        except mysql.connector.Error:
            stats["skipped"] += 1

    return user_map


def import_possessions(
    cursor,
    users: list[dict],
    user_map: dict[str, int],
    object_map: dict[str, tuple[int, str]],
    stats: dict[str, int],
) -> None:
    """Insère les possessions d'objets cosmétiques dans 'Possede'."""
    for user in users:
        username = clean_text(user.get("nomUtilisateur"))
        user_id = user_map.get(username)
        if user_id is None:
            continue

        # Le noeud 'achats' est optionnel dans la source.
        achats_node = user.get("achats")
        if not isinstance(achats_node, dict):
            continue

        for object_name in as_list(achats_node.get("objet")):
            name = clean_text(object_name)
            if not name:
                continue

            # On ne relie que les objets réellement importés plus tôt.
            object_entry = object_map.get(name)
            if object_entry is None:
                stats["skipped"] += 1
                continue

            object_id, _ = object_entry

            try:
                cursor.execute(
                    "INSERT IGNORE INTO Possede (idUtilisateur, idObjet) VALUES (%s, %s)",
                    (user_id, object_id),
                )
                if cursor.rowcount > 0:
                    stats["possessions"] += 1
            except mysql.connector.Error:
                stats["skipped"] += 1


def apply_active_objects(
    cursor,
    users: list[dict],
    user_map: dict[str, int],
    object_map: dict[str, tuple[int, str]],
    stats: dict[str, int],
) -> None:
    """Applique les objets actifs utilisateur (badge, titre, theme).

    La possession est verifiee avant update pour rester coherente avec les
    regles metier enforcees par trigger SQL.
    """
    active_specs = (
        ("badgeActif", "idBadgeActif", "badge"),
        ("titreActif", "idTitreActif", "titre"),
        ("themeActif", "idThemeActif", "theme"),
    )

    for user in users:
        username = clean_text(user.get("nomUtilisateur"))
        user_id = user_map.get(username)
        if user_id is None:
            continue

        for source_key, target_column, expected_type in active_specs:
            object_name = clean_text(user.get(source_key))
            if not object_name:
                continue

            # L'objet actif doit déjà exister dans la table d'objets importés.
            object_entry = object_map.get(object_name)
            if object_entry is None:
                stats["skipped"] += 1
                continue

            object_id, object_type = object_entry
            if object_type != expected_type:
                stats["skipped"] += 1
                continue

            # Vérification explicite côté import avant l'UPDATE final.
            cursor.execute(
                "SELECT 1 FROM Possede WHERE idUtilisateur = %s AND idObjet = %s",
                (user_id, object_id),
            )
            if cursor.fetchone() is None:
                stats["skipped"] += 1
                continue

            try:
                cursor.execute(
                    f"UPDATE Utilisateur SET {target_column} = %s WHERE idUtilisateur = %s",
                    (object_id, user_id),
                )
                if cursor.rowcount > 0:
                    stats["active_objects"] += 1
            except mysql.connector.Error:
                stats["skipped"] += 1
