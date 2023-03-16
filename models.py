"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

DEFAULT_IMG_URL = "https://www.seekpng.com/png/detail/297-2978586_rono-daniel-empty-profile-picture-icon.png"

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    first_name = db.Column(
        db.String(20),
        nullable=False
    )

    # Last name is optional for users
    last_name = db.Column(
        db.String(20),
    )

    image_url = db.Column(
        db.Text,
        default = DEFAULT_IMG_URL
    )

    def get_full_name(self):
        """Returns concat of first and last name"""
        if self.last_name:
            return self.first_name + ' ' + self.last_name
        else:
            return self.first_name

class Post(db.Model):
    """Post."""

    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    title = db.Column(
        db.String(65),
        nullable = False)

    content = db.Column(
        db.Text,
        nullable = False)

    created_at = db.Column(
        db.DateTime(timezone = True),
        nullable = True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'))

    user = db.relationship('User', backref='posts')



