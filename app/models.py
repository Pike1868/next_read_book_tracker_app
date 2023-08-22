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
    image_url = db.Column(db.Text, default="/static/images/default-pic.png")
    creation_date = db.Column(
        db.DateTime, nullable=False, default=datetime.now)
    hashed_password = db.Column(db.Text, nullable=False)

    books = db.relationship('UserBooks', backref='user', cascade='all, delete')

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


class Book(db.Model):
    """Books table..."""

    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    google_books_id = db.Column(db.Text, nullable=False, unique=True)
    isbn = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    author = db.Column(db.Text, nullable=False)
    thumbnail_url = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    published_date = db.Column(db.Date)

    users = db.relationship('UserBooks', backref='book', cascade='all, delete')


class UserBooks(db.Model):
    """UserBooks table..."""

    __tablename__ = 'user_books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id", ondelete='cascade'))
    book_id = db.Column(db.Integer, db.ForeignKey(
        "books.id", ondelete='cascade'))
    status = db.Column(db.String(50), nullable=False)
