import sqlite3
from sqlite3 import Error

def create_connection(db):
    """ Connect to a SQLite database """
    try:
        conn = sqlite3.connect(db)
        print(sqlite3.version)
    except Error as err:
        print(err)
    finally:
        conn.close()


if __name__ == '__main__':
    create_connection("pythonsqlite.db")