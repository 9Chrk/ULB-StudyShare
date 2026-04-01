"""Utilitaires d'initialisation de la base de données (exécution de script SQL)."""

import mysql.connector

from core.db.settings import DB_CONFIG


def execute_sql_script(filename: str) -> None:
    """Exécute un script SQL complet sur le serveur MySQL."""
    
    # On part de la configuration globale mais sans base sélectionnée
    config = DB_CONFIG.copy()
    del config['database']
    
    # Connexion à MySQL
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Lecture du script SQL
    with open(filename, 'r', encoding='utf-8') as f:
        script = f.read()

    # Exécution multi-statements
    cursor.execute(script)
    while cursor.nextset():
        pass

    connection.commit()
    cursor.close()
    connection.close()
