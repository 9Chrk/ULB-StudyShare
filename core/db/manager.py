"""Gestionnaire de contexte pour les connexions à la base de données."""

import mysql.connector

from core.db.settings import DB_CONFIG


class DBManager:
    """Ouvre une connexion MySQL et commit automatiquement si tout se passe bien."""

    def __enter__(self):
        """Crée la connexion et renvoie le curseur prêt à l'emploi."""
        self.connection = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Commit si aucune exception, puis ferme proprement curseur et connexion."""
        if exc_type is None:
            self.connection.commit()
        self.cursor.close()
        self.connection.close()
