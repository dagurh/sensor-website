"""Handles the database for the measurements web site"""
import sqlite3
from typing import Iterable, List

__MEASUREMENTS_DB = "measurements.db"
__CREATE_SQL = """
CREATE TABLE IF NOT EXISTS measurements
(temperature INTEGER NOT NULL,
 humidity INTEGER NOT NULL,
 pressure INTEGER NOT NULL,
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
        temperature (int): the temperature of the measurement
        humidity (int) : the humidity of the measurement
        pressure (int): the pressure of the measurement

    Returns:
        int: the number of rows affected (should be 1)
    """
    with sqlite3.connect(__MEASUREMENTS_DB) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO measurements VALUES (?,?,?,DATETIME('now', 'localtime'))", (temperature, humidity, pressure)
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


def all_measurements(paged) -> List:
    """Returns all the measurements in the DB

    Returns:
        List: a list of tuples
    """
    with sqlite3.connect(__MEASUREMENTS_DB) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT rowid,temperature,humidity,pressure,date
               FROM measurements
               ORDER BY rowid LIMIT 20 OFFSET ?;""", (20*paged,)
        )
        return cur.fetchall()

if __name__ != "__main__":
    create_database()
