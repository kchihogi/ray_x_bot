import sqlite3

class DB:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        return cursor.fetchall()

    def create_table(self, table_name, columns):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.execute_query(query)

    def insert(self, table_name, columns, values):
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        self.execute_query(query)

    def select(self, table_name, columns, where=None):
        if where:
            query = f"SELECT {columns} FROM {table_name} WHERE {where}"
        else:
            query = f"SELECT {columns} FROM {table_name}"
        return self.execute_query(query)

    def update(self, table_name, set, where):
        query = f"UPDATE {table_name} SET {set} WHERE {where}"
        self.execute_query(query)

    def delete(self, table_name, where):
        query = f"DELETE FROM {table_name} WHERE {where}"
        self.execute_query(query)

    def drop_table(self, table_name):
        query = f"DROP TABLE {table_name}"
        self.execute_query(query)

    def __del__(self):
        self.disconnect()

if __name__ == "__main__":
    db = DB("test.db")
    db.connect()
    db.create_table("tweets", "id INTEGER PRIMARY KEY, text TEXT, created_at TEXT")
    db.insert("tweets", "text, created_at", "'Hello, world!','2021-01-01 00:00:00'")
    print(db.select("tweets", "*"))
    db.disconnect()
