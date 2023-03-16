"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

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


