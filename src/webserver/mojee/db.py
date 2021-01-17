import os
import sqlite3

from flask import current_app, g


def get_db():
    db = getattr(g, "db", None)
    if db is None:
        query = open(current_app.config["SCHEMA"], "r").read()
        conn = sqlite3.connect(current_app.config["DATABASE"])
        cursor = conn.cursor()
        cursor.executescript(query)
        conn.commit()
        cursor.close()
        db = g._database = sqlite3.connect(current_app.config["DATABASE"])
    return db


def close_connection(exception):
    db = getattr(g, "db", None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_connection)
