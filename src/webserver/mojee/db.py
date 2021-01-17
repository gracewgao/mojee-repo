import os
import sqlite3

from flask import current_app, g

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "data/database.db")

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        query = open(app.config['SCHEMA'], 'r').read()
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()
        cursor.executescript(query)
        conn.commit()
        cursor.close()
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

# def get_db():
#     query = open(app.config['SCHEMA'], 'r').read()
#     conn = sqlite3.connect(app.config['DATABASE'])
#     cursor = conn.cursor()
#     cursor.executescript(query)
#     conn.commit()
#     cursor.close()
#     return sqlite3.connect(app.config['DATABASE'])

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_connection)
