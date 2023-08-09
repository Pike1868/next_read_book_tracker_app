from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""
    db.app = app

class User(db.Model, UserMixin):
    """User table..."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    bio = db.Column(db.Text)
    location = db.Column(db.Text)
    image_url = db.Column(db.Text,default="static/images/default-pic.png")
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    hashed_password = db.Column(db.Text, nullable=False)
    
    @property
    def formatted_date(self):
        """Return nicely-formatted date."""
        return self.creation_date.strftime("%a %b %-d  %Y, %-I:%M %p")
    
    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"
    
    @staticmethod
    def hash_password(password):
        return bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.hashed_password, password)
    
    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.hashed_password = User.hash_password(password)