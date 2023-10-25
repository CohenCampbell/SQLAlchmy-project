"""Blogly application."""
from flask import Flask, render_template, redirect, request
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)


db.create_all()


@app.route("/", methods=["POST", "GET"])
def root():
    edit = request.form.get("edit", False)
    first = request.form.get("first", None)
    last = request.form.get("last", None)
    url = request.form.get("url", None)
    if(url == ""):
        url = 'https://braverplayers.org/wp-content/uploads/2022/09/blank-pfp.png'

    if(first == None):
        return redirect("users")
    
    if(edit == "True"):
        userid = request.form.get("userData")
        user = User.get_by_id(userid)
        user.first_name = first
        user.last_name = last
        user.image_url = url
        db.session.commit()
        edit = False
        return redirect("/users")
    

    new_user = User(first_name=first, last_name=last, image_url=url)
    
    db.session.add(new_user)
    db.session.commit()
    
    return redirect("/users")

@app.route("/users")
def users():
    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/create")
def create():
    return render_template("create.html")

@app.route("/detail/<int:id>")
def details(id):
    user = User.query.get(id)
    return render_template("detail.html", user=user)

@app.route("/delete/<int:id>")
def delete(id):
    User.delete_user_byid(id)
    return redirect("/users")

@app.route("/edit<int:id>")
def edit(id):
    user = User.query.get(id)
    return render_template("edit.html", user=user)