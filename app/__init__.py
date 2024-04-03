from flask import Flask
from .models import db, connect_db, bcrypt
from .config import Config, Testing
from .routes.users import main_bp as main
from .routes.users import users_bp as users
from .routes.books import books_bp as books
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
load_dotenv()

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))


def create_app(config_name='Config'):
    """Flask Application Factory function: Creates the flask app context, initializes 
       extensions using the app instance, registers blueprints, returns the app."""

    app = Flask(__name__)

    # Dynamically select the configuration class based on the 'config_name' argument
    if config_name == 'Config':
        app.config.from_object(Config)
    elif config_name == 'Testing':
        app.config.from_object(Testing)
    else:
        raise ValueError("Invalid configuration name")

    connect_db(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'users_bp.sign_in'
    login_manager.login_message = "Please sign in to access this page/feature."
    login_manager.login_message_category = "danger"

    migrate = Migrate(app, db)

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(books)

    return app
