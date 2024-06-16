from uuid import uuid4
from os.path import join as path_join
import sqlite3


DB_NAME = "database.db"
DB_DIR = "db/"


class Database:
    def __init__(self, cwd) -> None:
        self.connection = sqlite3.connect(path_join(cwd, DB_DIR, DB_NAME))
        self.cursor = self.connection.cursor()
    
    def close(self) -> None:
        self.cursor.close()
        self.connection.close()

    def register_user(self, name: str, password_hash: str) -> None:
        uuid = str(uuid4())
        self.cursor.execute("INSERT INTO users(id, name, password_hash) VALUES (?, ?, ?);", 
                            (uuid, name, password_hash))
        self.connection.commit()
    
    def fetchuser_byname(self, name: str):
        res = self.cursor.execute("SELECT id, name FROM users WHERE name = ?;", (name,))
        if data := res.fetchone():
            return data
        return None
    
    