import sqlite3

def get_conn():
    conn = sqlite3.connect('tasklist')
    return conn