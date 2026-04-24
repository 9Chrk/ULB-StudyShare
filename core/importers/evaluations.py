"""Import des evaluations de resumes depuis le JSON commentaires."""

import mysql.connector

from core.importers.utils import bounded_int, clean_text


def import_evaluations(
    cursor,
    evaluations: list[dict],
    user_map: dict[str, int],
    resume_map: dict[tuple[str, str, str], int],
    stats: dict[str, int],
) -> None:
    """Insère les evaluations JSON quand auteur, destinataire et resume existent.

    La resolution du resume se fait via la cle metier
    '(destinataire, cours, titre)' construite pendant l'import des resumes.
    """
    for evaluation in evaluations:
        author_name = clean_text(evaluation.get("auteur"))
        recipient_name = clean_text(evaluation.get("destinataire"))
        resume_info = evaluation.get("resume") or {}

        if not isinstance(resume_info, dict):
            stats["skipped"] += 1
            continue

        code_cours = clean_text(resume_info.get("cours"))
        title = clean_text(resume_info.get("titre"))

        if not author_name or not recipient_name or not code_cours or not title:
            stats["skipped"] += 1
            continue

        author_id = user_map.get(author_name)
        recipient_id = user_map.get(recipient_name)
        if author_id is None or recipient_id is None:
            stats["skipped"] += 1
            continue

        # On filtre l'auto-evaluation cote import avant le trigger SQL.
        if author_id == recipient_id:
            stats["skipped"] += 1
            continue

        resume_id = resume_map.get((recipient_name, code_cours, title))
        if resume_id is None:
            stats["skipped"] += 1
            continue

        # Validation defensive pour respecter la contrainte CHECK(note BETWEEN 1 AND 5).
        note = bounded_int(evaluation.get("note"), default=1, minimum=1, maximum=5)
        comment = clean_text(evaluation.get("commentaire")) or None

        try:
            cursor.execute(
                """
                INSERT INTO Evalue (idUtilisateur, idResume, note, commentaire)
                VALUES (%s, %s, %s, %s)
                """,
                (author_id, resume_id, note, comment),
            )
            if cursor.rowcount > 0:
                stats["evaluations"] += 1

        except mysql.connector.Error:
            stats["skipped"] += 1
