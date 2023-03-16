"""Seed file to make sample data for blogly db."""

from models import User, db, Post
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
# An alternative if you don't want to drop
# and recreate your tables:
# Pet.query.delete()

# Add users
evan = User(first_name='Evan', last_name="Hesketh")
justin = User(first_name='Justin', last_name="Clark")
joel= User(first_name='Joel', last_name="Burton", image_url='http://joelburton.com/joel-burton.jpg')

# Add posts

post1 = Post(
    title="Test post 1",
    content="Text and info",
    user_id=1
    )

post2 = Post(
    title="Test post 2",
    content="Text and info",
    user_id=2
    )

post3 = Post(
    title="Test post 3",
    content="Text and info",
    user_id=3
    )

post4 = Post(
    title="Test post 4",
    content="Text and info",
    user_id=1
    )


# Add new objects to session, so they'll persist
db.session.add(evan)
db.session.add(justin)
db.session.add(joel)
db.session.add(post1)
db.session.add(post2)
db.session.add(post3)
db.session.add(post4)

# Commit--otherwise, this never gets saved!
db.session.commit()