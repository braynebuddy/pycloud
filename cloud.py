import math

import sql_data
import tag
import link

# Functions for generating word-cloud contents

def tags():
    tagid = tag.get_ids()
    linkid = link.get_ids()

    taglink = sql_data.get_taglinks()

    taglist = []
    max_count = 0
    min_count = 0
    max_size = 250
    min_size = 90

    linkcount = {}
    for tl in taglink:
        if taglink[tl][0] in linkcount:
            linkcount[taglink[tl][0]] = linkcount[taglink[tl][0]] + linkid[taglink[tl][1]][2]
        else:
            linkcount[taglink[tl][0]] = linkid[taglink[tl][1]][2]
        if linkcount[taglink[tl][0]] > max_count:
            max_count = linkcount[taglink[tl][0]]
        if min_count == 0 or linkcount[taglink[tl][0]] < min_count:
            min_count = linkcount[taglink[tl][0]]

    max_qty = math.log10(max_count)
    min_qty = math.log10(min_count)

    size_step = (max_size - min_size) / (max_qty - min_qty + 0.1)
    
    for id in sorted(tagid.items(), key=lambda kv:kv[1].casefold()):
        if id[0] in linkcount:
            tag_desc = tagid[id[0]] #f"Tag {i} Description"
            tag_url = id[0] # Tag ID
            tag_colr = f"#11f"
            tag_count = linkcount[id[0]] #linkid[i][2] #f"{4*i}"
            tag_size = int(min_size + (math.log10(linkcount[id[0]]) - min_qty) * size_step) #f"{100+2*id[0]}"
            taglist.append([tag_desc,tag_url,tag_size,tag_colr,tag_count])

    return taglist


def links(thetag):
    tagid = tag.get_ids()   # get all the tag information
    linkid = link.get_ids() # get all the link information

    taglinks = tag.get_links(thetag) # get a list of links that reference this tag

    max_count = 0
    min_count = 0
    max_size = 250
    min_size = 90

    for tl in taglinks:
        this_count = linkid[tl][2]
        if this_count > max_count:
            max_count = this_count
        if min_count == 0 or this_count < min_count:
            min_count = this_count

    max_qty = math.log10(max_count)
    min_qty = math.log10(min_count)

    size_step = (max_size - min_size) / (max_qty - min_qty + 0.1)

    linklist = []
    for id in sorted(linkid.items(), key=lambda v:v[1][0].casefold()):
        if id[0] in taglinks:
            link_id = id[0]
            link_desc = linkid[id[0]][0] # "Link {i} Description"
            link_url = linkid[id[0]][1] # Link {i} URL"
            link_size = int(min_size + (math.log10(linkid[id[0]][2]) - min_qty) * size_step) #f"{100+2*id[0]}"
            link_colr = f"#11f"
            link_count = linkid[id[0]][2] # Link {i} clicks"

            linklist.append([link_id,link_desc,link_url,link_size,link_colr,link_count])

    return linklist

def toptags():
    tagid = tag.get_ids()
    linkid = link.get_ids()

    taglink = sql_data.get_taglinks()

    max_count = 0
    min_count = 0
    max_size = 250
    min_size = 90

    linkcount = {}
    for tl in taglink:
        if taglink[tl][0] in linkcount:
            linkcount[taglink[tl][0]] = linkcount[taglink[tl][0]] + linkid[taglink[tl][1]][2]
        else:
            linkcount[taglink[tl][0]] = linkid[taglink[tl][1]][2]

    linkcount = dict(sorted(linkcount.items(), key = itemgetter(1), reverse = True)[:25])
    for t in linkcount:
        if t[1] > max_count:
            max_count = t[1]
        if t[1] < min_count or min_count == 0:
            min_count = t[1]
    
    max_qty = math.log10(max_count)
    min_qty = math.log10(min_count)

    size_step = (max_size - min_size) / (max_qty - min_qty + 0.1)
    
    taglist = []
    for id in sorted(tagid.items(), key=lambda kv:kv[1].casefold()):
        if id[0] in linkcount:
            tag_desc = tagid[id[0]] #f"Tag {i} Description"
            tag_url = id[0] # Tag ID
            tag_colr = f"#11f"
            tag_count = linkcount[id[0]] #linkid[i][2] #f"{4*i}"
            tag_size = int(min_size + (math.log10(linkcount[id[0]]) - min_qty) * size_step) #f"{100+2*id[0]}"
            taglist.append([tag_desc,tag_url,tag_size,tag_colr,tag_count])

    #top_tags = sorted(taglist, key=lambda v:v[4], reverse=True)[0:25]
    #return sorted(top_tags, key=lambda v:v[0])
    return taglist
