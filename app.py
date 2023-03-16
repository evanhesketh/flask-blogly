"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template, flash
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
    last_name = last_name if last_name else None
    image_url = request.form["image-url"]
    image_url = image_url if image_url else None

    if not first_name:
        flash('You must enter a first name')
        return render_template(
            "create_user.html",
            first_name=first_name,
            last_name=last_name,
            image_url=image_url
            )

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        image_url=image_url
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.get("/users/<int:user_id>")
def show_user_info(user_id):
    """Shows info for a given user, button to edit and
    button to delete"""

    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html', user=user)

@app.get("/users/<int:user_id>/edit")
def show_edit_user_page(user_id):
    """Shows edit page for a given user, button to cancel, button to save"""

    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.post("/users/<int:user_id>/edit")
def submit_edit_user_form(user_id):
    """Submits and updates user information, redirects to /users"""

    user = User.query.get_or_404(user_id)

    user.first_name = request.form["first-name"]
    user.last_name = request.form["last-name"]
    user.image_url = request.form["image-url"]

    if not user.first_name:
        flash('You must enter a first name')
        return render_template(
            "edit_user.html",
            user=user
            )

    db.session.commit()

    return redirect('/users')

@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Deletes a given user"""


    delete_user = User.query.get_or_404(user_id)

    User.query.filter(User.id == user_id).delete() #NOTE: Returns a 405, not 404

    db.session.commit()

    return redirect('/users')



