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
