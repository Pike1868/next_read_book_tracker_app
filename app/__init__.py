from flask import Flask
from .models import db, connect_db, bcrypt
from .config import Config
from .routes.main_routes import main
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager

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


def create_app(config_name):
    """Creates the flask app context"""
    app = Flask(__name__)
    app.config.from_object(f"app.config.{config_name}")
    toolbar = DebugToolbarExtension(app)
    connect_db(app)
    db.init_app(app)
    bcrypt.init_app(app)

    
    # While the object is instantiated at the module level, it is initialized inside the create_app function using the app instance.
    login_manager.init_app(app)
    
    # Register blueprints here
    app.register_blueprint(main)
    
    return app