from flask import Blueprint, render_template, redirect, flash, url_for, current_app
from sqlalchemy.exc import IntegrityError
from flask_login import current_user, login_user, logout_user, login_required
from ..models import User, db, UserBooks, Book
from ..forms import UserRegistrationForm, UserLoginForm, EditUserForm
from datetime import datetime
import os

TOP_GENRES = ["Romance", "Dystopian", "Mystery",
              "Fantasy", "Science Fiction", "Thriller"]


main_bp = Blueprint('main_bp', __name__)
users_bp = Blueprint('users_bp', __name__, url_prefix='/users')


@main_bp.route('/', methods=["GET"])
def home():
    """Displays the app homepage, depending on if user is signed in or anonymous"""
    form = UserRegistrationForm()
    if current_user.is_authenticated:
        users_books_previously_read = UserBooks.query.filter_by(
            user_id=current_user.id, status="previously_read").all()

        users_books_currently_reading = UserBooks.query.filter_by(
            user_id=current_user.id, status="currently_reading").all()

        users_books_want_to_read = UserBooks.query.filter_by(
            user_id=current_user.id, status="want_to_read").all()

        return render_template("/users/index.html", form=form, top_genres=TOP_GENRES, previously_read=[ub.book for ub in users_books_previously_read], currently_reading=[ub.book for ub in users_books_currently_reading], want_to_read=[ub.book for ub in users_books_want_to_read])
    else:
        return render_template("/users/index.html", form=form, top_genres=TOP_GENRES)


@users_bp.route('/sign_up', methods=["GET"])
def sign_up_form():
    """Displays user sign up form"""
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

        return redirect(url_for("main_bp.home"))

    return render_template("/users/sign_up.html", form=form)


@users_bp.route('/sign_in', methods=["GET"])
def sign_in_form():
    """Show sign in form"""
    form = UserLoginForm()

    return render_template("/users/sign_in.html", form=form)


@users_bp.route('/sign_in', methods=['POST'])
def sign_in():
    """Check user credentials, signs in user, logs failed sign in attempts"""
    if current_user.is_authenticated:
        flash("Your already logged in!")
        return redirect(url_for("main_bp.home"))

    form = UserLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f"Welcome Back, {current_user.username}!", "primary")
            return redirect(url_for("main_bp.home"))

        current_app.logger.info('User authentication failed')
        flash("Incorrect username or password", "danger")
    else:
        current_app.logger.info('Form not submitted or not validated')

    return render_template('/users/sign_in.html', form=form)


@users_bp.route("/profile", methods=["GET"])
@login_required
def user_profile():
    """Displays the user profile page"""

    return render_template("/users/profile.html")


@users_bp.route("/profile/edit",  methods=["GET"])
@login_required
def edit_user_form():
    """ Displays template for a user to edit their profile information"""
    form = EditUserForm()

    return render_template("/users/edit.html", form=form)


@users_bp.route("/profile/edit",  methods=["POST"])
@login_required
def edit_user_profile():
    """Handles user edit profile information form submission"""
    form = EditUserForm()

    if form.validate_on_submit():
        user = current_user

        if user.check_password(form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.bio = form.bio.data
            user.location = form.location.data
            user.image_url = form.image_url.data
            try:
                db.session.add(user)
                db.session.commit()
                flash("Profile updated successfully", "success")
                return redirect(url_for("users_bp.user_profile"))
            except IntegrityError:
                db.session.rollback()
                flash("Error, please select a new username or email", "danger")
        else:
            form.password.errors.append(
                "Incorrect password. Please enter your correct password to confirm changes.")
            return render_template("/users/edit.html", form=form)
    else:
        flash("Form validation failed, profile was not updated.", "danger")

    return redirect(url_for("users_bp.user_profile"))


@users_bp.route("/sign_out", methods=["POST"])
@login_required
def sign_out():
    """Signs out the current user and returns them to the homepage"""

    logout_user()
    flash("Goodbye!", "info")

    return redirect(url_for("main_bp.home"))


@users_bp.route("/delete", methods=["POST"])
@login_required
def delete_user_account():
    """Deletes user from db along with their saved book relationships in userbooks"""
    user = User.query.get_or_404(current_user.id)

    try:
        db.session.delete(user)
        db.session.commit()
        logout_user()
        current_app.logger.info(
            f'{user.username} deleted their account on {datetime.now()}')
        flash('Your account has been deleted.', 'success')
        return redirect(url_for('main_bp.home'))

    except Exception as e:
        current_app.logger.error(
            f'Error deleting account for user {user.username}: {e}')
        db.session.rollback()
        flash('There was an error deleting your account. Please try again.', 'danger')
        return redirect(url_for('users_bp.profile'))

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
