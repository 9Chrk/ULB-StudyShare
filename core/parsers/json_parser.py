"""Fonctions utilitaires pour parser des fichiers JSON."""

import json


def json_to_dict(file_path: str) -> list[dict[str, str]] | list[dict[str, list]]:
    """Lit un fichier JSON et retourne la première liste trouvée dans l'objet racine."""
    with open(file_path, mode="r", encoding="utf-8") as jsonfile:
        data = json.load(jsonfile)
        return data[list(data.keys())[0]]
