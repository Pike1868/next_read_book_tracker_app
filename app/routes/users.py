from flask import Blueprint, render_template, redirect, flash, url_for, current_app
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from ..models import User, db
from ..forms import UserRegistrationForm, UserLoginForm
from flask_restful import Api, Resource, reqparse

users = Blueprint('users', __name__)
api = Api(users)


def initialize_routes(api):
    api.add_resource(RegisterResource, '/register', endpoint="register")
    api.add_resource(LoginResource, '/login', endpoint="login")
    api.add_resource(LogoutResource, '/logout', endpoint="logout")


parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True,
                    help="Username cannot be blank!")
parser.add_argument('password', type=str, required=True,
                    help="Password cannot be blank!")
parser.add_argument('email', type=str, required=True,
                    help="Email cannot be blank!")

login_parser = reqparse.RequestParser()
login_parser.add_argument('login_email', type=str, required=True,
                    help="Email cannot be blank!")
login_parser.add_argument('login_password', type=str, required=True,
                    help="Password cannot be blank!")


@users.route('/', methods=["GET"])
def home_page():
    """Show app homepage"""
    register_form = UserRegistrationForm()
    login_form = UserLoginForm()

    return render_template("index.html", register_form=register_form, login_form=login_form)

class RegisterResource(Resource):
    def post(self):
        args = parser.parse_args()
        username = args.get('username')
        password = args.get('password')
        email = args.get('email')

        existing_username = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_username:
            return {'error': "Username is taken, please pick another."}, 400
        if existing_email:
            return {'error': "Email is already registered, please try logging in."}

        new_user = User(username=username, password=password, email=email)
        db.session.add(new_user)
        try:
            db.session.commit()
            login_user(new_user)
            print(f"{new_user.username} was logged in")
        except IntegrityError:
            return {"error": "Error in adding the user."}, 500

        return {"status": "success", "message": "Welcome! Successfully Created Your Account!"}, 200

class LoginResource(Resource):
    def post(self):
        args = login_parser.parse_args()
        email = args.get('login_email')
        password = args.get('login_password')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            return {"status": "success", 
                     "message": f"Welcome back, {user.username}!"}, 200
        else:
            current_app.logger.info('User authentication failed')
            return {"status": "error", "message":"Invalid email/password."}, 400

class LogoutResource(Resource):
    @login_required
    def post(self):
        logout_user()
        
        return {"status": "success", 
                     "message": f"Logout successful, goodbye."}, 200      
        