import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / 'clinic.db'


def connect(path=None):
    connection = sqlite3.connect(str(path or DB_PATH), timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute('PRAGMA foreign_keys = ON')
    return connection


def init_database(path=None):
    with connect(path) as db:
        schema = (Path(__file__).parent / 'sql' / 'schema.sql').read_text(encoding='utf-8')
        db.executescript(schema)
