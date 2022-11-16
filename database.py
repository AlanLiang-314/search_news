from secrets import token_urlsafe
import sqlite3

class saver:
    def __init__(self, path: str):
        self.path = path
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def insert(self, data: list):
        # id, url, type, title, content
        new_data = []
        for item in data:
            id = token_urlsafe(16)
            new_data.append((id, item))
        self.cur.executemany("INSERT INTO metadata VALUES(?, ?)", new_data)

    def delete(self, key: str):
        pass

    def find(self):
        data = self.cur.execute("SELECT * FROM metadata").fetchall()
        return data

    def commit(self):
        self.con.commit()
