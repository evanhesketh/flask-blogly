"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "secret"

connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.get("/")
def index():
    """Redirects to list of users"""
    return redirect("/users")

@app.get("/users")
def show_users():
    """Shows all users"""
    all_users = User.query.all()
    return render_template('users.html', users=all_users)

@app.get("/users/new")
def show_add_form():
    """Shows form to add new user"""
    return render_template('create_user.html')

@app.post("/users/new")
def add_new_user():
    """Process add user form and add user, redirects to /users"""
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")

@app.get("/users/<int:user_id>")
def show_user_info(user_id):
    """Shows info for a given user, button to edit and
    button to delete"""

@app.get("/users/<int:user_id>/edit")
def show_edit_user_page(user_id):
    """Shows edit page for a given user, button to cancel, button to save"""

@app.post("/users/<int:user_id>/edit")
def submit_edit_user_form(user_id):
    """Submits and updates user information, redirects to /users"""

@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Deletes a given user"""

