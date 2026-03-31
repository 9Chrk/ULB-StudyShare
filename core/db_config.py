import os
import mysql.connector
from dotenv import load_dotenv


# Charger les variables d'environnement depuis le fichier .env
load_dotenv() 

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
}


def execute_sql_script(filename):
    config = DB_CONFIG.copy()
    del config['database']
    
    # Connexion à MySQL
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Lecture du script SQL
    with open(filename, 'r', encoding='utf-8') as f:
        sql_commands = f.read().split(';')

    # Exécution ligne par ligne
    for command in sql_commands:
        command = command.strip()
        if command:
            cursor.execute(command)

    connection.commit()
    cursor.close()
    connection.close()
