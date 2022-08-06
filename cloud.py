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
    
    for id in sorted(tagid.items(), key=lambda kv:(kv[1], kv[0])):
        if id[0] in linkcount:
            tag_desc = tagid[id[0]] #f"Tag {i} Description"
            tag_url = f"http://tag{id[0]}.url"
            tag_colr = f"#11f"
            tag_count = linkcount[id[0]] #linkid[i][2] #f"{4*i}"
            tag_size = int(min_size + (math.log10(linkcount[id[0]]) - min_qty) * size_step) #f"{100+2*id[0]}"
            taglist.append([tag_desc,tag_url,tag_size,tag_colr,tag_count])

    return taglist


def links():
    tagid = tag.get_ids()
    linkid = link.get_ids()

    taglink = sql_data.get_taglinks()

    linklist = []

    return linklist