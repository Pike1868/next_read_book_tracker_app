from flask import Blueprint, render_template, redirect, flash, url_for, current_app
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from ..models import User, db
from ..forms import UserRegistrationForm, UserLoginForm

main = Blueprint('main', __name__)
# url_prefix='/main'


@main.route('/', methods=["GET"])
def home_page():
    """Show app homepage"""
    form = UserRegistrationForm()

    if current_user.is_authenticated:
        return redirect(url_for("main.logged_in_page"))

    return render_template("index.html", form=form)

@main.route('/register', methods=["POST"])
def register():
    """Handel user registration form submission"""
    form = UserRegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        existing_username = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_username:
            form.username.errors.append("Username taken, please pick another.")
            return redirect(url_for("main.home_page"))

        if existing_email:
            form.username.errors.append("Email is already is registered, please try logging in.")
            return redirect(url_for("main.login"))

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
            return render_template('index.html', form=form)
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect(url_for("main.logged_in_page"))

    return render_template("index.html", form=form)


@main.route('/login', methods=["GET"])
def show_login():
    """Show login form"""
    form = UserLoginForm()

    return render_template("login.html", form=form)


@main.route('/login', methods=['POST'])
def login():
    """Check user credentials, login user"""
    if current_user.is_authenticated:
        flash("Your already logged in!")
        return redirect(url_for("main.logged_in_page"))

    form = UserLoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f"Welcome Back, {current_user.username}!", "primary")
            return redirect(url_for("main.logged_in_page"))
        else:
            current_app.logger.info('User authentication failed')
            form.username.errors = ['Invalid username/password.']
    else:
        current_app.logger.info('Form not submitted or not validated')

    return render_template('login.html', form=form)


@main.route("/logged-in")
@login_required
def logged_in_page():

    return render_template("logged_in.html")


@main.route("/logout", methods=["POST"])
@login_required
def logout():

    logout_user()
    flash("Goodbye!", "info")

    return redirect(url_for("main.home_page"))
