import data

# Functions for managing tags

def get_ids():
    t = {}
    with data.create_connection('pycloud.db') as db:
        sql = "SELECT tag_id, name FROM menu_tag"
        cursor = db.execute(sql)
        for row in cursor:
            t[row[0]] = row[1] 
    return t

