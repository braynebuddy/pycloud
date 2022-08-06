import sqlite3
from sqlite3 import Error

# pycloud database access
def create_connection(fn):
    conn = None
    try:
        conn = sqlite3.connect(fn)
    except Error as e:
        conn = None
        print(e)
    return conn

def get_taglinks():
    t = {}
    with create_connection('pycloud.db') as db:
        sql = "SELECT taglink_id, tag_id, link_id FROM taglink"
        cursor = db.execute(sql)
        for row in cursor:
            t[row[0]] = [row[1], row[2]]
    return t
