from uuid import uuid4
import sqlite3


DB_NAME = "database.db"
DB = "sqlite:///" + DB_NAME

class Database:
    def __init__(self) -> None:
        self.connection = sqlite3.connect(DB)
        self.cursor = self.connection.cursor()
    
    def close(self) -> None:
        self.cursor.close()
        self.connection.close()

    def register_user(self, name: str, password_hash: str) -> None:
        uuid = uuid4()
        self.cursor.execute("INSERT INTO users(id, name, password_hash) VALUES (?, ?, ?)", 
                            (uuid, name, password_hash))
        self.connection.commit()
    
    