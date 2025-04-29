import sqlite3

class Database:
    def __init__(self):
        self.cursor = None
        self.connection = None

    def open_db(self, file_path):
        self.connection = sqlite3.connect(file_path)
        self.cursor = self.connection.cursor()

    def get_tables(self):
        return [row[0] for row in self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]

    def get_symbols(self, table_name):
        return [row[0] for row in self.cursor.execute(f"SELECT DISTINCT symbol FROM {table_name} ORDER BY symbol").fetchall()]

    def get_expiration_dates(self, paper_name, table_name):
        return [row[0] for row in self.cursor.execute(f"SELECT DISTINCT expiration FROM {table_name} WHERE symbol = '{paper_name}' ORDER BY expiration").fetchall()]

    def get_trading_dates(self, paper_name, table_name):
        return [row[0] for row in self.cursor.execute(f"SELECT DISTINCT date FROM {table_name} WHERE symbol = '{paper_name}' ORDER BY date").fetchall()]

    def close_db(self):
        if self.connection:
            self.connection.close()