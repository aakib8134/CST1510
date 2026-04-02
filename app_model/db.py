import sqlite3


def check_connection():
    conn = sqlite3.connect("DATA/intelligent_platform.db",
                           check_same_thread=False)
    return conn
