"""Import des resumes depuis la source utilisateurs XML."""

from typing import Optional

import mysql.connector

from core.importers.utils import as_list, clean_text, sql_datetime_or_now


def import_resumes(
    cursor,
    users: list[dict],
    user_map: dict[str, int],
    course_codes: set[str],
    year_code: str,
    stats: dict[str, int],
) -> dict[tuple[str, str, str], int]:
    """Insère les resumes puis retourne un index metier pour les evaluations.

    Returns:
        dict[tuple[str, str, str], int]: (auteur, cours, titre) -> idResume.
    """
    resume_map: dict[tuple[str, str, str], int] = {}

    for user in users:
        username = clean_text(user.get("nomUtilisateur"))
        user_id = user_map.get(username)
        if user_id is None:
            continue

        resumes_node = user.get("resumes")
        if not isinstance(resumes_node, dict):
            continue

        for resume in as_list(resumes_node.get("resume")):
            if not isinstance(resume, dict):
                stats["skipped"] += 1
                continue

            code_cours = clean_text(resume.get("cours"))
            title = clean_text(resume.get("titre"))
            date_publication = sql_datetime_or_now(resume.get("datePublication"))
            description = f"Résumé importé pour {code_cours}."

            # On conserve uniquement les resumes references par un cours connu.
            if not code_cours or not title or code_cours not in course_codes:
                stats["skipped"] += 1
                continue

            try:
                cursor.execute(
                    """
                    INSERT INTO Resume (titre, description, datePublication, idUtilisateur, codeCours, codeAnnee)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (title, description, date_publication, user_id, code_cours, year_code),
                )

                resume_id = cursor.lastrowid
                if not resume_id:
                    # Fallback défensif si le last row id n'est pas disponible.
                    resume_id = find_resume_id(cursor, user_id, code_cours, title)

                if resume_id is not None:
                    resume_map[(username, code_cours, title)] = resume_id
                    stats["resumes"] += 1
                else:
                    stats["skipped"] += 1
            except mysql.connector.Error:
                stats["skipped"] += 1

    return resume_map


def find_resume_id(cursor, user_id: int, code_cours: str, title: str) -> Optional[int]:
    """Recherche l'ID d'un resume existant via une cle metier simple."""
    cursor.execute(
        """
        SELECT idResume
        FROM Resume
        WHERE idUtilisateur = %s
          AND codeCours = %s
          AND titre = %s
        ORDER BY idResume DESC
        LIMIT 1
        """,
        (user_id, code_cours, title),
    )
    row = cursor.fetchone()
    return row[0] if row else None