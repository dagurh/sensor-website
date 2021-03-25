"""Handles the database for the Greetings web site"""
import sqlite3
from typing import Iterable, List

__GREETINGS_DB = "greetings.db"
__CREATE_SQL = """
CREATE TABLE IF NOT EXISTS greetings
(temperature TEXT NOT NULL,
 humidity TEXT NOT NULL,
 pressure TEXT NOT NULL,
 date TIMESTAMP NOT NULL);
"""


def create_database():
    """Creates the database"""
    with sqlite3.connect(
        __GREETINGS_DB, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    ) as conn:
        cur = conn.cursor()
        cur.execute(__CREATE_SQL)
        conn.commit()


def store_greeting(temperature: str, humidity: str, pressure: str) -> int:
    """Stores a greeting in the DB

    Args:
        temperature (str): the temperature of the greeting
        pressure (str): the pressure of the greeting

    Returns:
        int: the number of rows affected (should be 1)
    """
    with sqlite3.connect(__GREETINGS_DB) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO greetings VALUES (?,?,?,DATETIME('now'))", (temperature, humidity, pressure)
        )
        conn.commit()
        return cur.rowcount


def ten_greetings() -> List:
    """Returns all the greetings in the DB

    Returns:
        List: a list of tuples
    """
    with sqlite3.connect(__GREETINGS_DB) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT rowid,temperature,humidity,pressure,date
               FROM greetings
               ORDER BY rowid DESC LIMIT 10;"""
        )
        return cur.fetchall()

def all_greetings() -> List:
    """Returns all the greetings in the DB

    Returns:
        List: a list of tuples
    """
    with sqlite3.connect(__GREETINGS_DB) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT rowid,temperature,humidity,pressure,date
               FROM greetings
               ORDER BY rowid;"""
        )
        return cur.fetchall()



def get_greeting(rowid: int) -> tuple:
    """Gets a specific greeting

    Args:
        rowid (int): the rowid of the greeting in the DB

    Returns:
        tuple: the matching greeting
    """
    with sqlite3.connect(__GREETINGS_DB) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT rowid,temperature,humidity,pressure FROM greetings WHERE rowid = ?;",
            (rowid,),
        )
        return cur.fetchone()


def delete_greeting(rowid: int) -> int:
    """Deletes a specific greeting

    Args:
        rowid (int): the rowid of the greeting to be deleted

    Returns:
        int: the number of affected rows (0 or 1)
    """
    with sqlite3.connect(__GREETINGS_DB) as conn:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM greetings WHERE rowid = ?;",
            (rowid,),
        )
        conn.commit()
        return cur.rowcount




if __name__ != "__main__":
    create_database()
