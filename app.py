"""Blogly application."""
from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post, Tag, PostTag

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
    tags = Tag.query.all()
    users = User.query.all()
    return render_template("users.html", users=users, tags=tags)


@app.route("/create")
def create():
    return render_template("create.html")

@app.route("/detail/<int:id>")
def details(id):
    user = User.query.get(id)
    posts = Post.query.filter_by(user_id=id).all()
    return render_template("detail.html",posts=posts, user=user)

@app.route("/delete/<int:id>")
def delete(id):
    User.delete_user_byid(id)
    return redirect("/users")

@app.route("/edit<int:id>")
def edit(id):
    user = User.query.get(id)
    return render_template("edit.html", user=user)

@app.route("/post/<int:id>/new")
def new_posts(id):
    user = User.get_by_id(id)
    tags = Tag.query.all()
    return render_template("create_post.html", user=user, tags=tags)

@app.route("/post/add", methods=["POST"])
def create_posts():

    id = request.form["id"]
    title = request.form["title"]
    content = request.form["content"]
    tags_list = request.form.getlist("tag_checkboxes", None)
 
    new_post = Post(title=title, content=content, user_id=id)
    db.session.add(new_post)
    db.session.commit()

    for tag in tags_list:
        new_posttag = PostTag(post_id=new_post.id, tag_id=tag)
        db.session.add(new_posttag)

    db.session.commit()
    return redirect(f"/detail/{id}")

@app.route("/delete/post/<int:id>")
def delete_post(id):
    post = Post.query.get(id)
    uId = post.user_id
    del_posttag = PostTag.query.filter_by(post_id=id).all()
    for posttag in del_posttag:
        db.session.delete(posttag)
    Post.delete_post_byid(id)
    db.session.commit()
    return redirect(f"/detail/{uId}")

@app.route("/post/detail/<int:id>")
def post_detail(id):
    post = Post.query.get(id)
    user = User.query.get(post.user_id)
    tags = post.tags    
    
    return render_template("post_detail.html", post=post, user=user, tags=tags)

@app.route("/post/edit/<int:id>")
def edit_post(id):
    post = Post.query.get(id)
    tags = Tag.query.all()
    return render_template("edit_post.html", post=post, tags=tags)

@app.route("/edit/post/<int:id>", methods=["POST"])
def post_editor(id):

    del_tags = PostTag.query.filter_by(post_id=id).all()
    for tag in del_tags:
        db.session.delete(tag)
    db.session.commit()

    tags_list = request.form.getlist("tag_checkboxes", None)
    for tag in tags_list:
        new_posttag = PostTag(post_id=id, tag_id=tag)
        db.session.add(new_posttag)

    title = request.form["title"]
    content = request.form["content"]
    post = Post.query.get(id)
    post.title = title
    post.content = content
    db.session.commit()
    return redirect(f"/post/detail/{id}")

@app.route("/tag/create")
def tag_creater():
    return render_template("tag_create.html")

@app.route("/tag/create/post", methods=["POST"])
def tag_post_route():

    tag_name = request.form["tagname"]
    tag = Tag(name=tag_name)
    db.session.add(tag)
    db.session.commit()
    return redirect("/users")

@app.route("/tag/detail/<int:id>")
def tag_details(id):
    tag = Tag.query.get(id)
    posts = tag.posts
    print(posts)
    return render_template("tag_details.html", tag=tag, posts=posts)

@app.route("/tag/delete/<int:id>")
def tag_delete(id):
    Tag.delete_tag_byid(id)
    db.session.commit()
    return redirect("/users")

@app.route("/tag/edit/<int:id>")
def edit_tag(id):
    tag = Tag.query.get(id)
    return render_template("tag_edit.html", tag=tag)

@app.route("/tag/edit/post/<int:id>", methods=["POST"])
def tag_edit_post(id):
    tag = Tag.query.get(id)
    tag.name = request.form["tagname"]
    db.session.commit()
    return redirect("/users")