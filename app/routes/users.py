from flask import render_template, request, jsonify
from flask import Blueprint, render_template, redirect, flash, url_for, current_app, request
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from ..models import User, db
from ..forms import UserRegistrationForm, UserLoginForm, EditUserForm
import requests
import os

api_key = os.environ.get('API_KEY')

users_bp = Blueprint('users_bp', __name__)


@users_bp.route('/', methods=["GET"])
def home():
    """Show app homepage"""
    form = UserRegistrationForm()

    return render_template("/users/index.html", form=form)


@users_bp.route('/sign_up', methods=["GET"])
def sign_up_form():
    """Show user sign up form"""
    form = UserRegistrationForm()

    return render_template("/users/sign_up.html", form=form)


@users_bp.route('/sign_up', methods=["POST"])
def sign_up():
    """Handle user sign up form submission"""
    form = UserRegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        existing_username = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_username:
            form.username.errors.append("Username taken, please pick another.")
            return render_template("/users/sign_up.html", form=form)

        if existing_email:
            form.email.errors.append(
                "Email is already is registered, please try logging in.")
            return render_template("/users/sign_up.html", form=form)

        new_user = User(username=username, password=password, email=email)
        print(f"New User to add:{new_user}")
        db.session.add(new_user)
        try:
            db.session.commit()
            login_user(new_user)
            print("New User Added Successfully")
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            print("Error")
            return render_template('/users/index.html', form=form)
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect(url_for("users_bp.home"))

    return render_template("/users/sign_up.html", form=form)


@users_bp.route('/sign_in', methods=["GET"])
def sign_in_form():
    """Show sign in form"""
    form = UserLoginForm()

    return render_template("/users/sign_in.html", form=form)


@users_bp.route('/sign_in', methods=['POST'])
def sign_in():
    """Check user credentials, sign_in user"""
    if current_user.is_authenticated:
        flash("Your already logged in!")
        return redirect(url_for("users_bp.home"))

    form = UserLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f"Welcome Back, {current_user.username}!", "primary")
            return redirect(url_for("users_bp.home"))
        else:
            current_app.logger.info('User authentication failed')
            form.username.errors = ['Invalid username/password.']
    else:
        current_app.logger.info('Form not submitted or not validated')

    return render_template('/users/sign_in.html', form=form)


@users_bp.route("/profile", methods=["GET"])
@login_required
def user_profile():

    return render_template("/users/profile.html")


@users_bp.route("/profile/edit",  methods=["GET"])
@login_required
def edit_user_form():
    form = EditUserForm()

    return render_template("/users/edit.html", form=form)

# Should be a PUT method?


@users_bp.route("/profile/edit",  methods=["POST"])
@login_required
def edit_user_profile():
    form = EditUserForm()

    if form.validate_on_submit():
        user = current_user
        user.username = form.username.data
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.bio = form.bio.data
        user.location = form.location.data
        user.image_url = form.image_url.data
        try:
            print(user)
            db.session.add(user)
            db.session.commit()
            flash("Profile updated successfully", "success")
            return redirect(url_for("users_bp.user_profile"))
        except IntegrityError:
            db.session.rollback()
            flash("Error, please select a new username or email")
    else:
        flash("Form validation failed, profile was not updated.", "danger")
        return redirect(url_for("users_bp.user_profile"))


@users_bp.route("/logout", methods=["POST"])
@login_required
def logout():

    logout_user()
    flash("Goodbye!", "info")

    return redirect(url_for("users_bp.home"))

##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask


@users_bp.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
