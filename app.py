from datetime import datetime, timezone
import calendar
import logging

from flask import Flask, flash, render_template, redirect, request, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps

# Import models and db instance from models.py
from models import User, ExternalUser, Project, Skill, Experience, Testimonial, ContactMessage, MessageThread, db

app = Flask(__name__)
app.config.from_object('config')  # Load configuration from config.py

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"  # Set the login view for Flask-Login

# Initialize the database
with app.app_context():
    db.init_app(app)
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('You do not have permission to access this page.')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    projects = Project.query.all()
    skills = Skill.query.all()
    testimonials = Testimonial.query.all()
    return render_template('index.html', projects=projects, skills=skills, testimonials=testimonials)


if __name__ == "__main__":
    app.run(debug=True, port=8000)