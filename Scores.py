import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


class HighScores:

    def __init__(self):
        self.scores_database = "scores.db"
        create_scores_table = """CREATE TABLE IF NOT EXISTS scores(id INTEGER PRIMARY KEY AUTOINCREMENT, name text NOT NULL,
         score INTEGER);"""
        self.conn = create_connection(self.scores_database)
        self.cursor = self.conn.cursor()
        if self.conn is not None:
            create_table(self.conn, create_scores_table)
        else:
            print("Error! cannot create the database connection.")

    def add_score(self, score):
        add = f'''INSERT INTO scores(name, score) VALUES(?, ?)'''
        self.cursor.execute(add, score)
        return self.cursor.lastrowid

    def get_scores(self):
        self.cursor.execute("SELECT name, score FROM scores ORDER BY score DESC")
        rows = self.cursor.fetchall()
        scores = []
        for row in rows:
            scores.append(row)
        return scores

    def get_highscore(self):
        pass