import logging
from flask import Flask
from flask import render_template
from flask import redirect, request, session
from flask_session import Session

from pycloud import sql_data
from pycloud import tag
from pycloud import link
from pycloud import cloud

def create_app(testing: bool = True):
    app = Flask(__name__)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    
    Session(app)

    # -------------------
    # Main Menu Page
    # -------------------
    @app.route('/')
    @app.route('/index')
    def index():
        if session.get("name"):
            return render_template('home.html', 
                            tag_list=cloud.tags(25), 
                            link_list=cloud.toplinks(25))
        else:
            return redirect("/login")

    # -------------------
    # Login and Logout
    # -------------------
    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/dologin', methods=['POST','GET'])
    def dologin():
        if request.method == "POST":
            email = request.form.get("email")
            passwd = request.form.get("passwd")
            db = sql_data.create_connection()
            if db:
                sql = "SELECT email, passwd, name FROM menu_user"
                cursor = db.execute(sql)
                for row in cursor:
                    if email==row[0] and passwd==row[1]:
                        session["name"] = row[2]
                db.close()
        return redirect("/index")

    @app.route('/logout')
    def logout():
        session["name"] = None
        return redirect("/login")

    # -------------------
    # Cloud of tags
    # -------------------
    @app.route('/tags')
    def tags():
        if session.get("name"):
            return render_template('tags.html', 
                                tag_list=cloud.tags(-1))
        else:
            return redirect("/login")

    # ----------------------
    # Cloud of URLs (links)
    # ----------------------
    @app.route('/links/<int:tagid>')
    def links(tagid):
        if session.get("name"):
            return render_template('links.html', 
                                tag_name=tag.get_name(tagid), 
                                link_list=cloud.links(tagid))
        else:
            return redirect("/login")

    @app.route('/alllinks')
    def alllinks():
        if session.get("name"):
            return render_template('links.html', 
                                tag_name="All Links", 
                                link_list=cloud.links(0))
        else:
            return redirect("/login")


    @app.route('/admin')
    def admin():
        if session.get("name"):
            return render_template('admin.html', 
                                link_list=cloud.links(0),
                                tag_list=cloud.tags(-1))
        else:
            return redirect("/login")

    @app.route('/link_detail')
    def show_link():
        if session.get("name"):
            return render_template('admin.html', 
                                link_list=cloud.links(0))
        else:
            return redirect("/login")

    @app.route('/tag_detail')
    def show_tag():
        if session.get("name"):
            return render_template('admin.html', 
                                link_list=cloud.tags(-1))
        else:
            return redirect("/login")

    # ----------------------
    # Server-side Helpers
    # ----------------------
    @app.route('/linkcount/<int:link_id>')
    def linkcount(link_id):
        clicks = link.incr_clicks(link_id)
        return redirect(request.referrer)

    @app.route('/add_link', methods=['POST','GET'])
    def add_link():
        if request.method == "POST":
            link_name = request.form.get("name")
            link_url = request.form.get("url")
            link.create(link_name, link_url)
        return redirect("/admin")

    @app.route('/add_tag', methods=['POST','GET'])
    def add_tag():
        if request.method == "POST":
            tag_name = request.form.get("name")
            app.logger.error(f"NOT IMPLEMENTED: Tag Name is '{tag_name}'")
        return redirect("/admin")

    return app
