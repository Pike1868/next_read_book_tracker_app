from flask import Flask
from .models import db, connect_db, bcrypt
from .config import Config
from .routes.users import users, api, initialize_routes
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate

# export FLASK_APP="app:create_app('Config')"
# for testing: export FLASK_APP="app:create_app('Testing')"

# instantiated at the module level
login_manager = LoginManager()

# The User Loader function tells Flask-Login how to find a specific user object based on their ID
@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))


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
    login_manager.login_view = 'users.login'
    login_manager.login_message = "Please login in to access this page."
    login_manager.login_message_category = "danger"

    migrate = Migrate(app, db)

    app.register_blueprint(users)
    # Api needs to be initialized before adding routes
    api.init_app(app)  
    initialize_routes(api)

    return app
