from flask import Flask
from flask import render_template
from flask import redirect, request, session
from flask_session import Session
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
@app.route('/index')
def index():
    if session.get("name"):
        name = session.get("name")
        return render_template('home.html', page_title='PyCloud Menu', page_heading='The PyCloud', username=name)
    else:
        return redirect("/login")

@app.route('/login')
def login():
    return render_template('login.html', page_title='PyCloud Login', page_heading='PyCloud')

@app.route('/dologin', methods=['POST','GET'])
def dologin():
    if request.method == "POST":
        email = request.form.get("email")
        passwd = request.form.get("passwd")
        db = create_connection('pycloud.db')
        if db:
            sql = "SELECT email, passwd, name FROM menu_user"
            cursor = db.execute(sql)
            for row in cursor:
                if email==row[0] and passwd==row[1]:
                    session["name"] = row[2]
            db.close()
    return redirect("/index")

@app.route('/add/<int:n1>/<int:n2>/')
def add(n1, n2):
    return '<h1>{}</h1>'.format(n1 + n2)

@app.route('/tags')
def tags():
    return render_template('tags.html', page_title='PyCloud Menu', page_heading='PyCloud', tag_list=tag_content())

@app.route('/links')
def links():
    return render_template('links.html', page_title='PyCloud Menu', page_heading='PyCloud')

@app.route('/logout')
def logout():
    session["name"] = None
    return redirect("/login")

def create_connection(fn):
    conn = None
    try:
        conn = sqlite3.connect(fn)
    except Error as e:
        conn = None
        print(e)
    return conn

def get_tagid():
    t = {}
    with create_connection('pycloud.db') as db:
        sql = "SELECT tag_id, name FROM menu_tag"
        cursor = db.execute(sql)
        for row in cursor:
            t[row[0]] = row[1] 
    return t

def get_taglink():
    t = {}
    with create_connection('pycloud.db') as db:
        sql = "SELECT taglink_id, tag_id, link_id FROM taglink"
        cursor = db.execute(sql)
        for row in cursor:
            t[row[0]] = [row[1], row[2]]
    return t

def get_linkid():
    l = {}
    with create_connection('pycloud.db') as db:
        sql = "SELECT link_id, name, url, clicks FROM menu_link"
        cursor = db.execute(sql)
        for row in cursor:
            l[row[0]] = [row[1], row[2], row[3]]
    return l

def tag_content():
    tagid = get_tagid()
    taglink = get_taglink()
    linkid = get_linkid()

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

    size_step = (max_size - min_size) / (max_count - min_count + 1)
    
    for id in sorted(tagid.items(), key=lambda kv:(kv[1], kv[0])):
        if id[0] in linkcount:
            tag_desc = tagid[id[0]] #f"Tag {i} Description"
            tag_url = f"http://tag{id[0]}.url"
            tag_colr = f"#11f"
            tag_count = linkcount[id[0]] #linkid[i][2] #f"{4*i}"
            tag_size = int(min_size + (linkcount[id[0]] - min_count) * size_step) #f"{100+2*id[0]}"
            taglist.append([tag_desc,tag_url,tag_size,tag_colr,tag_count])

    return taglist
