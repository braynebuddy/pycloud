from pycloud import sql_data

# Functions for working with links (i.e., URLs)

def get_ids():
    l = {}
    with sql_data.create_connection() as db:
        sql = "SELECT link_id, name, url, clicks FROM menu_link"
        cursor = db.execute(sql)
        for row in cursor:
            l[row[0]] = [row[1], row[2], row[3]]
    return l

def get_id(url):
    link_data = get_ids()
    for key, value in link_data.items():
        if value[1].strip() == url.strip():
            return key
    return -1

def incr_clicks(linkid):
    current_clicks = 0
    with sql_data.create_connection() as db:
        sql = f"SELECT clicks FROM menu_link WHERE link_id={linkid}"
        cursor = db.execute(sql)
        for row in cursor:
            current_clicks = row[0]
        current_clicks += 1
        sql = f"UPDATE menu_link SET clicks={current_clicks} WHERE link_id={linkid}"
        cursor = db.execute(sql)
    return current_clicks

def get_top(numlinks):
    if numlinks < 1:
        numlinks = 99999
    # get all the link information
    linkid = get_ids()     
    # return the top "numlinks" sorted by number of clicks
    return dict(sorted(linkid.items(), key = lambda v:v[1][2], reverse = True)[:numlinks]) 

def existing(url):
    # Check see if this link URL exists in the database
    return False if get_id(url) < 0 else True

def create(name, url):
    # Don't add this link if input is blank or URL already exists
    if name == "" or url == "" or existing(url):
        return False

    # Get rid of non-alphanumerics in name
    link_name = ''.join(filter(str.isalnum, name))

    # Add the new link to the database
    with sql_data.create_connection() as db:
        sql = f"INSERT INTO menu_link (name,url,clicks) VALUES ('{link_name}','{url.strip()}',1)"
        cursor = db.execute(sql)
    return True

def update(name, url = "", clicks = -1):
    # Get rid of non-alphanumerics in name
    link_name = ''.join(filter(str.isalnum, name))

    # Only update if this link already exists
    linkid = get_id(url)
    if linkid >= 0:
        # Update the link url information
        if not url == "":
            with sql_data.create_connection() as db:
                sql = f"UPDATE menu_link SET url={url.strip()} WHERE link_id={linkid}"
                cursor = db.execute(sql)
        # Update the link clicks information
        if clicks >= 0:
            with sql_data.create_connection() as db:
                sql = f"UPDATE menu_link SET clicks={clicks} WHERE link_id={linkid}"
                cursor = db.execute(sql)
    return

def delete(name):
    # Get rid of non-alphanumerics in name
    link_name = ''.join(filter(str.isalnum, name))

    # Check to make sure this link already exists
    linkid = get_id(url)
    if linkid >= 0:
        # Remove any tag linkages
        with sql_data.create_connection() as db:
            sql = "SELECT taglink_id, tag_id, link_id FROM taglink"
            cursor = db.execute(sql)
            for row in cursor:
                if row[2] == linkid:
                    sql = f"DELETE FROM taglink WHERE WHERE taglink_id={row[0]}"
                    cursor_2 = db.execute(sql)

        # Delete the link
        with sql_data.create_connection() as db:
            sql = f"DELETE FROM menu_link WHERE WHERE link_id={linkid}"
            cursor = db.execute(sql)
    return
