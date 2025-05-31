from core import db_manager
from core.db_manager import DBManager

def check(username, password):
  with DBManager() as cursor:
    cursor.execute(
      "SELECT * FROM Utilisateur WHERE NomUtilisateur = %s AND MotDePasse = %s",
      (username, password)
    )
    return cursor.fetchone() is not None

def add(username, password):
  with DBManager() as cursor:
    cursor.execute(
      "SELECT * FROM Utilisateur WHERE NomUtilisateur = %s",
      (username,)
    )
    if cursor.fetchone():
      return False
    
    cursor.execute(
      "INSERT INTO Utilisateur (NomUtilisateur, MotDePasse) VALUES (%s, %s)",
      (username, password)
    )
    return True
