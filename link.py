import sql_data

# Functions for working with links (i.e., URLs)

def get_ids():
    l = {}
    with sql_data.create_connection('pycloud.db') as db:
        sql = "SELECT link_id, name, url, clicks FROM menu_link"
        cursor = db.execute(sql)
        for row in cursor:
            l[row[0]] = [row[1], row[2], row[3]]
    return l

def incr_clicks(linkid):
    current_clicks = 0
    with sql_data.create_connection('pycloud.db') as db:
        sql = f"SELECT clicks FROM menu_link WHERE link_id={linkid}"
        cursor = db.execute(sql)
        for row in cursor:
            current_clicks = row[0]
        current_clicks += 1
        sql = f"UPDATE menu_link SET clicks={current_clicks} WHERE link_id={linkid}"
        cursor = db.execute(sql)
    return current_clicks
