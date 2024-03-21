"""Models for Blogly."""
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement = True)
    first_name = db.Column(db.Text,
                           nullable=False)
    last_name = db.Column(db.Text,
                           nullable=False)
    img_url = db.Column(db.Text,
                       nullable = False,
                       default = DEFAULT_IMAGE_URL)
    
    posts = db.relationship('Post', backref='user', cascade="all, delete-orphan")

    
    @property
    def full_name(self):
        

        return f"{self.first_name} {self.last_name}"
    
class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text,
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime,
                           default=datetime.datetime.now
                           )
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'), nullable=False)
    
    @property
    def friendly_date(self):
        return self.created_at.strftime("%m-%d-%Y %H:%M")
    
class Tag(db.Model):

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text,
                     unique=True,
                     nullable=False)   
    
    posts = db.relationship(
        'Post',
        backref="tags",
        secondary="posts_tags",
        cascade="all,delete"
    ) 

class PostTag(db.Model):

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        nullable=False,
                        primary_key=True)
    
    tag_id = db.Column(db.Integer,
                        db.ForeignKey('tags.id'),
                        nullable=False,
                        primary_key=True)

    
    
    
def connect_db(app):
    with app.app_context():
        db.app = app
        db.init_app(app)
        
    
    

