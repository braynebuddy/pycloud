from flask import Flask
from flask import render_template
from flask import redirect, request, session
from flask_session import Session

import pycloud.sql_data
import pycloud.tag
import pycloud.link
import pycloud.cloud

def create_app(testing: bool = True):
    app = Flask(__name__)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    @app.route('/')
    @app.route('/index')
    def index():
        if session.get("name"):
            name = session.get("name")
            return render_template('home.html', page_title='PyLynx Menu', page_heading='The PyLynx', username=name, tag_list=pycloud.cloud.tags(25), link_list=pycloud.cloud.toplinks(25))
        else:
            return redirect("/login")

    @app.route('/login')
    def login():
        return render_template('login.html', page_title='PyLynx Login', page_heading='PyLynx')

    @app.route('/dologin', methods=['POST','GET'])
    def dologin():
        if request.method == "POST":
            email = request.form.get("email")
            passwd = request.form.get("passwd")
            db = sql_data.create_connection('pycloud.db')
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
        return render_template('tags.html', page_title='PyLynx Menu', page_heading='PyLynx', tag_list=pycloud.cloud.tags(-1))

    @app.route('/links/<int:tagid>')
    def links(tagid):
        return render_template('links.html', page_title='PyLynx Menu', page_heading='PyLynx', tag_name=pycloud.tag.get_name(tagid), link_list=pycloud.cloud.links(tagid))

    @app.route('/alllinks')
    def alllinks():
        return render_template('links.html', page_title='PyLynx Menu', page_heading='PyLynx', tag_name="All Links", link_list=pycloud.cloud.links(0))

    @app.route('/logout')
    def logout():
        session["name"] = None
        return redirect("/login")

    @app.route('/linkcount/<int:link_id>')
    def linkcount(link_id):
        clicks = pycloud.link.incr_clicks(link_id)
        return redirect(request.referrer)

    return app
