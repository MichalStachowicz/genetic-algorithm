import sqlite3
from config import name

db_name = f"database{name}.db"


def create_table():
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS individuals(
                                                energy REAL,
                                                generation_number INTEGER,
                                                status TEXT)""")
    conn.commit()
    conn.close()


def insert_to_db(energy, generation, status):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("INSERT INTO individuals VALUES(?,?,?)", (energy, generation, status))
    conn.commit()
    conn.close()


create_table()
