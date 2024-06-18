from uuid import uuid4
from os.path import join, exists
import sqlite3


DB_NAME = "database.db"
DB_DIR = "db/"

class Database:
    def __init__(self, cwd) -> None:
        db_path = join(cwd, DB_DIR, DB_NAME)

        if (not exists(db_path)):
            file = open(db_path, "w")
            file.close()

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            with open(join(cwd, DB_DIR, "schema.sql"), "r") as sql_script:
                cursor.executescript(sql_script.read())

            conn.commit()
            cursor.close()
            conn.close()

        self.connection = sqlite3.connect(db_path)
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
        res = self.cursor.execute("SELECT * FROM users WHERE name = ?;", (name,))
        if data := res.fetchone():
            return data
        return None
    
    def fetch_history(self, user_id: str):
        res = self.cursor.execute("SELECT datetime, initial_video, second_video FROM history WHERE user_id = ?;", (user_id,))
        if data := res.fetchall():
            return data
        return None
    
    def add_commit(self, user_id: str, initialvideo: str, secondvideo: str):
        self.cursor.execute("INSERT INTO history(user_id, initial_video, second_video) VALUES (?, ?, ?);", 
                            (user_id, initialvideo, secondvideo))
        self.connection.commit()
    
    