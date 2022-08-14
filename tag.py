import sql_data

# Functions for managing tags

def get_ids():
    t = {}
    with sql_data.create_connection('pycloud.db') as db:
        sql = "SELECT tag_id, name FROM menu_tag"
        cursor = db.execute(sql)
        for row in cursor:
            t[row[0]] = row[1] 
    return t

def get_name(tagid):
    tagname = "None"
    with sql_data.create_connection('pycloud.db') as db:
        sql = "SELECT tag_id, name FROM menu_tag"
        cursor = db.execute(sql)
        for row in cursor:
            if row[0] == tagid:
                tagname = row[1] 
    return tagname

def get_links(tagid):
    linklist = []
    with sql_data.create_connection('pycloud.db') as db:
        sql = "SELECT taglink_id, tag_id, link_id FROM taglink"
        cursor = db.execute(sql)
        for row in cursor:
            if row[1] == tagid or tagid == 0:
                linklist.append(row[2])
    return linklist
