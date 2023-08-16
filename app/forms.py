from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from .models import User, UserMixin, db

    

class UserRegistrationForm(FlaskForm):
    """Form for user registration/sign-up"""
    username = StringField('Username', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    confirm = PasswordField("Confirm password",validators=[DataRequired(),EqualTo("password", message="Password fields must match."),
        ],
    )
        
class UserLoginForm(FlaskForm):
    """Form for user login"""
    
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    