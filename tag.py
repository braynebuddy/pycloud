from pycloud import sql_data

# Functions for managing tags

def get_all():
    t = {}
    with sql_data.create_connection() as db:
        sql = "SELECT tag_id, name FROM menu_tag"
        cursor = db.execute(sql)
        for row in cursor:
            t[row[0]] = row[1] 
    return t

def get_name(tagid):
    tagname = ""
    with sql_data.create_connection() as db:
        sql = "SELECT tag_id, name FROM menu_tag"
        cursor = db.execute(sql)
        for row in cursor:
            if row[0] == tagid:
                tagname = row[1] 
    return tagname

def get_id(tagname):
    tagid = -1
    with sql_data.create_connection() as db:
        sql = f"SELECT tag_id, name FROM menu_tag WHERE name='{tagname.strip()}'"
        cursor = db.execute(sql)
        for row in cursor:
            if row[1].strip() == tagname.strip():
                tagid = int(row[0])
    return tagid

def get_info(tagid):
    with sql_data.create_connection() as db:
        sql = f"SELECT tag_id, name FROM menu_tag WHERE tag_id={int(tagid)}"
        cursor = db.execute(sql)
        for row in cursor:
            if int(row[0]) == int(tagid):
                return [int(row[0]), row[1]]
    return []


def get_links(tagid):
    linklist = []
    with sql_data.create_connection() as db:
        sql = "SELECT taglink_id, tag_id, link_id FROM taglink"
        cursor = db.execute(sql)
        for row in cursor:
            if row[1] == tagid or tagid == 0:
                linklist.append(row[2])
    return linklist

def exists(tagname):
    # Check see if this tag exists in the database
    return False if get_id(tagname) < 0 else True

def create(tagname):
    # Don't add this tag if it already exists
    if  exists(tagname):
        return False

    # Get rid of non-alphanumerics in name
    #link_name = ''.join(filter(str.isalnum, name))
    #print(f"Changed link name from '{name}' to '{link_name}'")

    # Add the new link to the database
    with sql_data.create_connection() as db:
        sql = f"INSERT INTO menu_tag (name) VALUES ('{tagname}')"
        #print (sql)
        cursor = db.execute(sql)
    return True
    
def update(tagid, tagname):

    # Only update if this tag already exists
    the_tag = get_info(tagid)
    if len(the_tag) > 0:

        # Update the link name information
        if not tagname == "":
            with sql_data.create_connection() as db:
                sql = f"UPDATE menu_tag SET name='{tagname.strip()}' WHERE tag_id={tagid}"
                cursor = db.execute(sql)

    return

def delete(tagid):
    # Check to make sure this tag already exists
    the_tag = get_info(tagid)
    if len(the_tag) > 0:
        # Remove any tag linkages
        with sql_data.create_connection() as db:
            sql = f"DELETE FROM taglink WHERE tag_id={tagid}"
            #print (sql)
            cursor = db.execute(sql)

        # Delete the tag
        with sql_data.create_connection() as db:
            sql = f"DELETE FROM menu_tag WHERE tag_id={tagid}"
            cursor = db.execute(sql)
    return
