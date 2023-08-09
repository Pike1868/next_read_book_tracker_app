from flask import Blueprint, render_template, redirect, request, flash, url_for
from ..models import User

main = Blueprint('main', __name__)

@main.route('/')
def home_page():
    """Show app homepage"""
    
    
    return render_template("index.html")