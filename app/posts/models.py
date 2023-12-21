from datetime import datetime
from app import db
from sqlalchemy import Enum

post_tag = db.Table('post_tag',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.String, nullable=False)
    image_file = db.Column(db.String, default='postdefault.jpg')
    created = db.Column(db.TIMESTAMP, default=datetime.now)
    type = db.Column(db.Enum('news', 'publication', 'other'), default='other')
    enabled = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('posts', uselist=False))
    tags = db.relationship('Tag', secondary=post_tag, backref=db.backref('posts', lazy=True))


    def __repr__(self):
        return f"Post {self.id}: {self.title}."
        

class Category(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return f"Category {self.id}: {self.name}."


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return f"Tag {self.id}: {self.name}."