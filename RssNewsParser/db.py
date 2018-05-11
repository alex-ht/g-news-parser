# -*- coding: utf-8 -*-
import sqlite3
import os
def open_or_create_db(path):
    if os.path.isfile(path):
        return sqlite3.connect(path)
    else:
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute('CREATE TABLE news(key TEXT PRIMARY KEY, source TEXT, date TEXT, content TEXT, wave TEXT, youtube_key INTEGER UNIQUE)')
        conn.commit()
        return conn;

def close_db(conn):
    conn.commit()
    conn.close()

def insert_record(conn, key, source, date, content, wave, youtube_key):
    c = conn.cursor()
    c.execute('INSERT INTO news VALUES (%s, %s, %s, %s, %s, %d)' % (key, source, date, content, wave, int(youtube_key)))
