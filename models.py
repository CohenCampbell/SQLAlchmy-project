from flask_sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()

class User(db.Model):
    __tablename__ = 'users'

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)
    
    @classmethod
    def delete_user_byid(cls, id):
        user_del = cls.query.get(id)
        db.session.delete(user_del)
        db.session.commit()
        return
    
    @classmethod
    def get_full_name(cls, first, last):
        return cls.query.filter(cls.first_name == first, cls.last_name == last).all()

    id = db.Column(db.Integer,
               primary_key=True,
               autoincrement=True
               )

    first_name = db.Column(db.Text,
                           nullable=False,
                           unique=True)
    
    last_name = db.Column(db.Text,
                           nullable=False,
                           unique=True)
    
    image_url = db.Column(db.Text, 
                          default='https://braverplayers.org/wp-content/uploads/2022/09/blank-pfp.png',
                          nullable=False
                          )
    
    post = db.relationship("Post")

class Post(db.Model):
    __tablename__ = "posts"

    @classmethod
    def delete_post_byid(cls, id):
        user_del = cls.query.get(id)
        db.session.delete(user_del)
        db.session.commit()
        return

    id = db.Column(db.Integer,
               primary_key=True,
               autoincrement=True
               )
    
    title = db.Column(db.Text,
                      nullable=False)
    
    content = db.Column(db.Text,
                        nullable=False)
    
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.now)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User')
                           