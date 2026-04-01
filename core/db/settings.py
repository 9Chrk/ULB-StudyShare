import os
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
