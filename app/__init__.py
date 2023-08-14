from flask import Flask
from .models import db, connect_db, bcrypt
from .config import Config
from .routes.main_routes import main
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_restful import Api

# Set flask app environment variable with cmd below before flask run
# export FLASK_APP="app:create_app('Config')"
# for testing: export FLASK_APP="app:create_app('Testing')"

# instantiated at the module level
login_manager = LoginManager()

# The User Loader function tells Flask-Login how to find a specific user object based on they're ID


@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))


api = Api()


def create_app(config_name):
    """Flask Application Factory function: Creates the flask app context, initializes 
       extensions using the app instance, registers blueprints, returns the app."""

    app = Flask(__name__)
    app.config.from_object(f"app.config.{config_name}")
    connect_db(app)

    toolbar = DebugToolbarExtension(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message = "Please login in to access this page."
    login_manager.login_message_category = "danger"

    migrate = Migrate(app, db)

    app.register_blueprint(main)
    api.init_app(app)

    return app
