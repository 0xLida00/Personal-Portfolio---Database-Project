from datetime import datetime, timezone
from sqlalchemy import cast, Date
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


# --------------- User Authentication Routes ---------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if not user:
            flash(f"No such user '{username}'")
            return redirect(url_for("login"))
        if password != user.password:
            flash(f"Invalid password for the user '{username}'")
            return redirect(url_for("login"))

        login_user(user)
        flash(f"Welcome back, {username}!")
        return redirect(url_for("index"))
    return render_template("auth/login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))
        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))
        # Check if the email already exists
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))
        # Create a new user instance and store the password as plain text
        new_user = User(username=username, email=email, password=password)

        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


# --------------- User Profile Routes ---------------
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = current_user
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

    return render_template('auth/profile.html', user=user)


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    user = User.query.get_or_404(current_user.user_id)
    
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        # Check if the current password is correct
        if not user.check_password(current_password):  # Assuming `check_password()` method exists
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('change_password'))

        # Check if new passwords match
        if new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
            return redirect(url_for('change_password'))

        # Update password
        user.set_password(new_password)  # Assuming `set_password()` method exists
        db.session.commit()
        flash('Password updated successfully!', 'success')
        return redirect(url_for('profile'))

    return render_template('auth/change_password.html')


@app.route('/delete_profile', methods=['POST'])
@login_required
def delete_profile():
    # Assuming current_user is the user to be deleted
    try:
        db.session.delete(current_user)
        db.session.commit()
        flash('Profile deleted successfully!', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        flash('An error occurred. Profile could not be deleted.', 'danger')
        return redirect(url_for('profile'))


if __name__ == "__main__":
    app.run(debug=True, port=8000)