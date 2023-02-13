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
    app.logger.setLevel(gunicorn_logger.level)
    
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
            #print(f"Validating with {email} - {passwd}")
            db = sql_data.create_connection()
            if db:
                sql = "SELECT email, passwd, name FROM menu_user"
                cursor = db.execute(sql)
                for row in cursor:
                    #print(f"Found {row[0]} - {row[1]}")
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
                                tag_name="", 
                                link_list=cloud.links(0))
        else:
            return redirect("/login")


    # ----------------------
    # Database Administration
    # ----------------------
    @app.route('/admin')
    def admin():
        if session.get("name"):
            return render_template('admin.html', 
                                link_list=cloud.links(0),
                                tag_list=cloud.tags(-1))
        else:
            return redirect("/login")

    # ----------------------
    # Details
    # ----------------------
    @app.route('/link_detail', methods=['POST','GET'])
    def show_link():
        if session.get("name"):
            if request.method == "POST":
                selected = request.form.get("link")
            selected_link = link.get_by_url(selected)
            #print(f"Selected link name: '{selected}'")
            #print(f"Selected link: '{selected_link}'")
            #print(f"Link tags: '{link.get_tags(selected_link[0])}'")

            return render_template('link_detail.html', 
                                  link=selected_link,
                                  linktags=link.get_tags(selected_link[0]),
                                  alltags=cloud.tags(-1))
        else:
            return redirect("/login")

    @app.route('/tag_detail', methods=['POST','GET'])
    def show_tag():
        if session.get("name"):
            if request.method == "POST":
                selected = request.form.get("tagid")
            return render_template('tag_detail.html', 
                                tag=tag.get_info(selected))
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
            res = link.create(link_name, link_url)
            if not res:
                app.logger.error(f"ADD LINK: Not added: '{link_name}', '{link_url}'")
        return redirect("/admin")

    @app.route('/modify_link', methods=['POST','GET'])
    def modify_link():
        if request.method == "POST":
            if request.form['action'] == "Update":
                link_id = int(request.form.get("id"))
                link_name = request.form.get("name")
                link_url = request.form.get("url")
                link_clicks = int(request.form.get("clicks"))
                link_tags = list(map(int, request.form.getlist("checked_tags")))
                #print (f"UPDATE: {link_id}.{link_name} URL='{link_url}' Clicks={link_clicks}")
                #print (f"UPDATE: taglist = {link_tags}")
                link.update(link_id, url=link_url, name=link_name, clicks=link_clicks, taglist=link_tags)
            
            if request.form['action'] == "Delete":
                link_url = request.form.get("url")
                #print (f"DELETE: '{link_url}'")
                link.delete(link_url)
        return redirect("/admin")

    @app.route('/add_tag', methods=['POST','GET'])
    def add_tag():
        if request.method == "POST":
            tag_name = request.form.get("name")
            res = tag.create(tag_name)
            if not res:
                app.logger.error(f"ADD TAG: Not added: '{tag_name}'")
        return redirect("/admin")

    @app.route('/modify_tag', methods=['POST','GET'])
    def modify_tag():
        if request.method == "POST":
            if request.form['action'] == "Update":
                tag_id = int(request.form.get("id"))
                tag_name = request.form.get("name")
                #print (f"UPDATE: {tag_id}.{tag_name}")
                tag.update(tag_id, name=tag_name)
            
            if request.form['action'] == "Delete":
                tag_id = int(request.form.get("id"))
                #print (f"DELETE: '{tag_id}'")
                tag.delete(tag_id)
        return redirect("/admin")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()