"""Fonctions utilitaires pour parser des fichiers CSV."""

import csv


def csv_to_dict(file_path: str) -> list[dict[str, str]]:
    """Lit un fichier CSV et retourne une liste de lignes sous forme de dictionnaires."""
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        data = csv.DictReader(csvfile)
        return [row for row in data]
