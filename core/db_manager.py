import mysql.connector
from core.db_config import DB_CONFIG

class DBManager:
  def __enter__(self):
    self.connection = mysql.connector.connect(**DB_CONFIG)
    self.cursor = self.connection.cursor()
    return self.cursor

  def __exit__(self, exc_type, exc_val, exc_tb):
    if exc_type is None:
      self.connection.commit()
    self.cursor.close()
    self.connection.close()
