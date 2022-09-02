from pycloud import sql_data

# Functions for working with links (i.e., URLs)

def get_all():
    links = {}
    with sql_data.create_connection() as db:
        sql = "SELECT link_id, name, url, clicks FROM menu_link"
        cursor = db.execute(sql)
        for row in cursor:
            links[int(row[0])] = [row[1], row[2], int(row[3])]
    #for key,value in l.items():
    #    print(f"key: {key}, value: {value}") 
    return links

def get_by_id(id):
    with sql_data.create_connection() as db:
        sql = f"SELECT link_id, name, url, clicks FROM menu_link WHERE link_id={id}"
        cursor = db.execute(sql)
        for row in cursor:
            if int(row[0]) == int(id):
                return [int(row[0]), row[1], row[2], int(row[3])]
    return []

def get_by_name(name):
    with sql_data.create_connection() as db:
        sql = f"SELECT link_id, name, url, clicks FROM menu_link WHERE name='{name.strip()}'"
        cursor = db.execute(sql)
        for row in cursor:
            if row[1].strip() == name.strip():
                return [int(row[0]), row[1], row[2], int(row[3])]
    return []

def get_by_url(url):
    with sql_data.create_connection() as db:
        sql = f"SELECT link_id, name, url, clicks FROM menu_link WHERE url='{url.strip()}'"
        cursor = db.execute(sql)
        for row in cursor:
            if row[2].strip() == url.strip():
                return [int(row[0]), row[1], row[2], int(row[3])]
    return []

def incr_clicks(linkid):
    current_clicks = 0
    with sql_data.create_connection() as db:
        sql = f"SELECT clicks FROM menu_link WHERE link_id={linkid}"
        cursor = db.execute(sql)
        for row in cursor:
            current_clicks = int(row[0])
        current_clicks += 1
        sql = f"UPDATE menu_link SET clicks={current_clicks} WHERE link_id={linkid}"
        cursor = db.execute(sql)
    return current_clicks

def get_tags(linkid):
    taglist = []
    with sql_data.create_connection() as db:
        sql = "SELECT taglink_id, tag_id, link_id FROM taglink"
        cursor = db.execute(sql)
        for row in cursor:
            if int(row[2]) == int(linkid):
                taglist.append(int(row[1]))
    return taglist

def get_top(numlinks):
    if numlinks < 1:
        numlinks = 99999
    # get all the link information
    linkinfo = get_all()     
    # return the top "numlinks" sorted by number of clicks
    return dict(sorted(linkinfo.items(), key = lambda v:v[1][2], reverse = True)[:numlinks]) 

def exists(url):
    # Check see if this link URL exists in the database
    return False if len(get_by_url(url)) == 0 else True

def create(name, url, clicks = 1):
    # Don't add this link if input is blank or URL already exists
    if name == "" or url == "" or exists(url):
        return False

    # Get rid of non-alphanumerics in name
    #link_name = ''.join(filter(str.isalnum, name))
    #print(f"Changed link name from '{name}' to '{link_name}'")

    # Add the new link to the database
    with sql_data.create_connection() as db:
        sql = f"INSERT INTO menu_link (name,url,clicks) VALUES ('{name}','{url.strip()}',{clicks})"
        #print (sql)
        cursor = db.execute(sql)
    return True

def update(id, url = "", name = "", clicks = -1, taglist = []):
    # Get rid of non-alphanumerics in name
    #link_name = ''.join(filter(str.isalnum, name))

    # Only update if this link already exists
    link = get_by_id(id)
    if len(link) > 0:

        # Update the link name information
        if not name == "":
            with sql_data.create_connection() as db:
                sql = f"UPDATE menu_link SET name='{name.strip()}' WHERE link_id={link[0]}"
                cursor = db.execute(sql)

        # Update the link url information if this URL is not already there
        if not url == "" and not exists(url.strip()):
            with sql_data.create_connection() as db:
                sql = f"UPDATE menu_link SET url='{url.strip()}' WHERE link_id={link[0]}"
                cursor = db.execute(sql)

        # Update the link clicks information
        if clicks >= 0:
            with sql_data.create_connection() as db:
                sql = f"UPDATE menu_link SET clicks={clicks} WHERE link_id={link[0]}"
                cursor = db.execute(sql)

        # Update list of tags associated with this link        
        if len(taglist) > 0:
            current_taglist = get_tags(link[0])
            print (f"Tag list: {taglist}")
            print (f"Current tag list: {current_taglist}")
            # Add missing taglist tags
            for tag in taglist:
                if not int(tag) in current_taglist:
                    with sql_data.create_connection() as db:
                        sql = f"INSERT INTO taglink (tag_id, link_id) VALUES ({tag},{link[0]})"
                        print (sql)
                        cursor = db.execute(sql)
            # Remove current tags not in taglist
            for tag in current_taglist:
                if not int(tag) in taglist:
                    with sql_data.create_connection() as db:
                        sql = f"DELETE FROM taglink WHERE tag_id={tag} AND link_id={link[0]}"
                        print (sql)
                        cursor = db.execute(sql)
    return

def delete(url):
    # Get rid of non-alphanumerics in name
    #link_name = ''.join(filter(str.isalnum, name))

    # Check to make sure this link already exists
    link = get_by_url(url)
    if len(link) > 0:
        # Remove any tag linkages
        with sql_data.create_connection() as db:
            sql = f"DELETE FROM taglink WHERE link_id={link[0]}"
            #print (sql)
            cursor = db.execute(sql)

        # Delete the link
        with sql_data.create_connection() as db:
            sql = f"DELETE FROM menu_link WHERE link_id={link[0]}"
            cursor = db.execute(sql)
    return
