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

# Add new objects to session, so they'll persist
db.session.add(evan)
db.session.add(justin)
db.session.add(joel)

# Commit--otherwise, this never gets saved!
db.session.commit()