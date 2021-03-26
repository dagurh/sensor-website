"""Handles the database for the Greetings web site"""
import sqlite3
from typing import Iterable, List

__MEASUREMENTS_DB = "measurements.db"
__CREATE_SQL = """
CREATE TABLE IF NOT EXISTS measurements
(temperature TEXT NOT NULL,
 humidity TEXT NOT NULL,
 pressure TEXT NOT NULL,
 date TIMESTAMP NOT NULL);
"""


def create_database():
    """Creates the database"""
    with sqlite3.connect(
        __MEASUREMENTS_DB, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    ) as conn:
        cur = conn.cursor()
        cur.execute(__CREATE_SQL)
        conn.commit()


def store_measurement(temperature: str, humidity: str, pressure: str) -> int:
    """Stores a measurement in the DB

    Args:
        temperature (str): the temperature of the measurement
        pressure (str): the pressure of the measurement

    Returns:
        int: the number of rows affected (should be 1)
    """
    with sqlite3.connect(__MEASUREMENTS_DB) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO measurements VALUES (?,?,?,DATETIME('now'))", (temperature, humidity, pressure)
        )
        conn.commit()
        return cur.rowcount


def ten_measurements() -> List:
    """Returns all the measurements in the DB

    Returns:
        List: a list of tuples
    """
    with sqlite3.connect(__MEASUREMENTS_DB) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT rowid,temperature,humidity,pressure,date
               FROM measurements
               ORDER BY rowid DESC LIMIT 10;"""
        )
        return cur.fetchall()

def max_temp():
    with sqlite3.connect(__MEASUREMENTS_DB) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT MAX(temperature)
               FROM measurements"""
        )
        return cur.fetchone()

def min_temp():
    with sqlite3.connect(__MEASUREMENTS_DB) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT MIN(temperature)
               FROM measurements"""
        )
        return cur.fetchone()

def max_hum():
    with sqlite3.connect(__MEASUREMENTS_DB) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT MAX(humidity)
               FROM measurements"""
        )
        return cur.fetchone()

def min_hum():
    with sqlite3.connect(__MEASUREMENTS_DB) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT MIN(humidity)
               FROM measurements"""
        )
        return cur.fetchone()

def max_pres():
    with sqlite3.connect(__MEASUREMENTS_DB) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT MAX(pressure)
               FROM measurements"""
        )
        return cur.fetchone()

def min_pres():
    with sqlite3.connect(__MEASUREMENTS_DB) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT MIN(pressure)
               FROM measurements"""
        )
        return cur.fetchone()


def all_measurements() -> List:
    """Returns all the measurements in the DB

    Returns:
        List: a list of tuples
    """
    with sqlite3.connect(__MEASUREMENTS_DB) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT rowid,temperature,humidity,pressure,date
               FROM measurements
               ORDER BY rowid;"""
        )
        return cur.fetchall()



def get_measurement(rowid: int) -> tuple:
    """Gets a specific measurement

    Args:
        rowid (int): the rowid of the measurement in the DB

    Returns:
        tuple: the matching measurement
    """
    with sqlite3.connect(__MEASUREMENTS_DB) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT rowid,temperature,humidity,pressure FROM measurements WHERE rowid = ?;",
            (rowid,),
        )
        return cur.fetchone()


def delete_measurement(rowid: int) -> int:
    """Deletes a specific measurement

    Args:
        rowid (int): the rowid of the measurement to be deleted

    Returns:
        int: the number of affected rows (0 or 1)
    """
    with sqlite3.connect(__MEASUREMENTS_DB) as conn:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM measurements WHERE rowid = ?;",
            (rowid,),
        )
        conn.commit()
        return cur.rowcount




if __name__ != "__main__":
    create_database()