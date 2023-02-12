import math
from operator import itemgetter

from pycloud import sql_data
from pycloud import tag
from pycloud import link

# Functions for generating word-cloud contents

def links(thetag):
    tagid    = tag.get_all()   # get all the tag information
    linkid   = link.get_all() # get all the link information
    taglinks = tag.get_links(thetag) # get a list of links that reference this tag

    max_count = 0
    min_count = 0
    max_size = 250
    min_size = 100

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
        if id[0] in taglinks or thetag == 0:
            link_id = id[0]
            link_desc = linkid[id[0]][0] # "Link {i} Description"
            link_url = linkid[id[0]][1] # Link {i} URL"
            if linkid[id[0]][2] == 0:
                link_size = int(min_size + (math.log10(1) - min_qty) * size_step) #f"{100+2*id[0]}"
            else:
                link_size = int(min_size + (math.log10(linkid[id[0]][2]) - min_qty) * size_step) #f"{100+2*id[0]}"
            link_colr = f"#11f"
            link_count = linkid[id[0]][2] # Link {i} clicks"

            linklist.append([link_id,link_desc,link_url,link_size,link_colr,link_count])

    return linklist

def tags(numtags):
    tagid   = tag.get_all()
    linkid  = link.get_all()
    taglink = sql_data.get_taglinks()

    if numtags < 1:
        numtags = 9999

    max_count = 0
    min_count = 0
    max_size = 250
    min_size = 100

    linkcount = {}
    for t in tagid:
        linkcount[t] = 0

    for tl in taglink:
        if taglink[tl][0] in linkcount:
            linkcount[taglink[tl][0]] = linkcount[taglink[tl][0]] + linkid[taglink[tl][1]][2]
        else:
            linkcount[taglink[tl][0]] = linkid[taglink[tl][1]][2]

    linkcount = dict(sorted(linkcount.items(), key = itemgetter(1), reverse = True)[:numtags])
    for t in linkcount:
        if linkcount[t] > max_count:
            max_count = linkcount[t]
        if linkcount[t] > 0 and (linkcount[t] < min_count or min_count == 0):
            min_count = linkcount[t]
    
    max_qty = math.log10(max_count)
    min_qty = math.log10(min_count)

    size_step = (max_size - min_size) / (max_qty - min_qty + 0.1)
    
    taglist = []
    for id in sorted(tagid.items(), key=lambda kv:kv[1].casefold()):
        if id[0] in linkcount:
            tag_desc = tagid[id[0]] #f"Tag {i} Description"
            tag_id = id[0] # Tag ID
            tag_colr = f"#11f"
            tag_count = linkcount[id[0]] #linkid[i][2] #f"{4*i}"
            tag_size = int(min_size + (math.log10(linkcount[id[0]]) - min_qty) * size_step) #f"{100+2*id[0]}"
            taglist.append([tag_desc,tag_id,tag_size,tag_colr,tag_count])

    return taglist

def toplinks(numlinks):
    tagid  = tag.get_all()   # get all the tag information
    linkid = link.get_top(numlinks) # get the top link information

    #if numlinks < 1:
    #    numlinks = 99999
    #linkid = dict(sorted(linkid.items(), key = lambda v:v[1][2], reverse = True)[:numlinks]) # get the top numlinks

    max_count = 0
    min_count = 0
    max_size = 250
    min_size = 100

    for lk in linkid:
        this_count = linkid[lk][2]
        if this_count > max_count:
            max_count = this_count
        if min_count == 0 or this_count < min_count:
            min_count = this_count

    max_qty = math.log10(max_count)
    min_qty = math.log10(min_count)

    size_step = (max_size - min_size) / (max_qty - min_qty + 0.1)

    linklist = []
    for id in sorted(linkid.items(), key=lambda v:v[1][0].casefold()):
        link_id = id[0]
        link_desc = linkid[id[0]][0] # "Link {i} Description"
        link_url = linkid[id[0]][1] # Link {i} URL"
        link_size = int(min_size + (math.log10(linkid[id[0]][2]) - min_qty) * size_step) #f"{100+2*id[0]}"
        link_colr = f"#11f"
        link_count = linkid[id[0]][2] # Link {i} clicks"

        linklist.append([link_id,link_desc,link_url,link_size,link_colr,link_count])

    return linklist
