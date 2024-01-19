import sqlite3

CREATE_SCORE_TABLE = 'CREATE TABLE SCORE (id INTEGER PRIMARY KEY, score INTEGER);'

INSERT_SCORE = 'INSERT INTO SCORE (score) VALUES (?);'

GET_HIGHEST_SCORE = "SELECT MAX(score) FROM SCORE;"


def connect():
    return sqlite3.connect('data.db')


def create_tables(connection):
    with connection:
        try:
            connection.execute(CREATE_SCORE_TABLE)
        except sqlite3.OperationalError:
            pass


def add_score(connection, score):
    with connection:
        connection.execute(INSERT_SCORE, (score,))


def get_highest_score(connection):
    with connection:
        return connection.execute(GET_HIGHEST_SCORE).fetchone()

