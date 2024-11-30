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


# --------------- Projects & Manage Projects Routes ---------------
@app.route('/projects')
def projects():
    projects = Project.query.all()
    return render_template('portfolio/projects.html', projects=projects)

@app.route('/manage_projects')
@login_required
@admin_required
def manage_projects():
    projects = Project.query.all()
    return render_template('dashboard/manage_projects.html', projects=projects)

@app.route('/add_project', methods=['POST'])
@login_required
@admin_required
def add_project():
    title = request.form['title']
    description = request.form['description']
    technologies = request.form['technologies']
    link = request.form.get('link')  # Get the optional link field
    user_id = current_user.user_id  # Ensure the user_id is set to the current user's ID

    # Create a new project instance with the provided data
    project = Project(user_id=user_id, title=title, description=description, technologies=technologies, link=link)
    db.session.add(project)
    db.session.commit()
    flash('Project added successfully.', 'success')
    return redirect(url_for('manage_projects'))


@app.route('/edit_project/<int:project_id>', methods=['POST'])
@login_required
@admin_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    project.title = request.form['title']
    project.description = request.form['description']
    project.technologies = request.form['technologies']

    # Only update link if provided (optional)
    link = request.form.get('link')
    if link:
        project.link = link

    db.session.commit()
    flash('Project updated successfully.', 'success')
    return redirect(url_for('manage_projects'))


@app.route('/delete_project/<int:project_id>', methods=['GET'])
@login_required
@admin_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)

    try:
        db.session.delete(project)
        db.session.commit()
        flash(f'Project "{project.title}" has been successfully deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Failed to delete project "{project.title}". Please try again.', 'danger')
        print(f"Error deleting project: {e}")

    return redirect(url_for('manage_projects'))


# --------------- Skills & Manage Skills Routes ---------------
@app.route('/skills')
def skills():
    skills = Skill.query.all()
    return render_template('portfolio/skills.html', skills=skills)


@app.route('/manage_skills')
@login_required
@admin_required
def manage_skills():
    skills = Skill.query.all()
    return render_template('dashboard/manage_skills.html', skills=skills)


@app.route('/add_skill', methods=['POST'])
@login_required
def add_skill():
    skill_name = request.form['skill_name']
    proficiency_level = request.form['proficiency_level']
    category = request.form.get('category', None)
    active = request.form['active'] == 'True'  # Convert string to boolean
    new_skill = Skill(
        skill_name=skill_name,
        proficiency_level=proficiency_level,
        category=category,
        active=active,
        user_id=current_user.user_id
    )
    
    db.session.add(new_skill)
    db.session.commit()
    flash('Skill added successfully!', 'success')
    return redirect(url_for('manage_skills'))


@app.route('/edit_skill', methods=['POST'])
@login_required
def edit_skill():
    skill_id = request.form['skill_id']
    skill = Skill.query.get_or_404(skill_id)
    skill.skill_name = request.form['skill_name']
    skill.proficiency_level = request.form['proficiency_level']
    skill.category = request.form.get('category', None)
    skill.active = request.form['active'] == 'True'  # Convert string to boolean
    
    db.session.commit()
    flash('Skill updated successfully!', 'success')
    return redirect(url_for('manage_skills'))


@app.route('/delete_skill/<int:skill_id>', methods=['GET'])
@login_required
@admin_required
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    try:
        db.session.delete(skill)
        db.session.commit()
        flash(f'Skill "{skill.skill_name}" has been successfully deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Failed to delete skill "{skill.skill_name}". Please try again.', 'danger')
        print(f"Error deleting skill: {e}")
    return redirect(url_for('manage_skills'))


# --------------- Experiences & Manage Experiences Routes ---------------
@app.route('/experiences')
def experiences():
    experiences = Experience.query.all()
    return render_template('portfolio/experiences.html', experiences=experiences)


@app.route('/manage_experiences')
@login_required
def manage_experiences():
    experiences = Experience.query.all()
    return render_template('dashboard/manage_experiences.html', experiences=experiences)


@app.route('/add_experience', methods=['POST'])
@login_required
def add_experience():
    # Retrieve form data
    position = request.form['position']
    company = request.form['company']
    start_date_str = request.form['start_date']
    end_date_str = request.form['end_date'] if request.form['end_date'] else None
    description = request.form['description']
    # Convert the start_date and end_date to date objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()  # Convert start_date string to date object
    end_date = None
    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()  # Convert end_date string to date object if provided
    # Assuming user_id is already set for the logged-in user
    user_id = current_user.user_id
    # Create a new experience object
    new_experience = Experience(
        user_id=user_id,
        position=position,
        company=company,
        start_date=start_date,
        end_date=end_date,
        description=description
    )
    # Add the new experience to the database
    db.session.add(new_experience)
    db.session.commit()

    flash('Experience added successfully!', 'success')
    return redirect(url_for('manage_experiences'))


@app.route('/edit_experience/<int:experience_id>', methods=['POST'])
@login_required
def edit_experience(experience_id):
    experience = Experience.query.get_or_404(experience_id)
    experience.position = request.form['position']
    experience.company = request.form['company']
    start_date_str = request.form['start_date']
    end_date_str = request.form['end_date'] if request.form['end_date'] else None
    experience.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()

    if end_date_str:
        experience.end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    else:
        experience.end_date = None

    experience.description = request.form['description']
    
    db.session.commit()
    flash('Experience updated successfully!', 'success')
    return redirect(url_for('manage_experiences'))


@app.route('/delete_experience/<int:experience_id>', methods=['POST'])
@login_required
def delete_experience(experience_id):
    experience = Experience.query.get_or_404(experience_id)
    db.session.delete(experience)
    db.session.commit()

    flash('Experience deleted successfully!', 'success')
    return redirect(url_for('manage_experiences'))


# --------------- Contact & Messages Routes ---------------
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if not name or not email or not message:
            flash("All fields are required. Please fill out the form completely.", "danger")
            return redirect(url_for('contact'))
        try:
            external_user = ExternalUser.query.filter_by(email=email).first()
            if not external_user:
                external_user = ExternalUser(
                    first_name=name.split()[0] if len(name.split()) > 0 else "",
                    last_name=" ".join(name.split()[1:]),
                    email=email,
                    platform="Website",
                    user_id=current_user.user_id if current_user.is_authenticated else None
                )
                db.session.add(external_user)
                db.session.commit()

            contact_message = ContactMessage(
                external_user_id=external_user.external_user_id,
                user_id=current_user.user_id if current_user.is_authenticated else None,
                name=name,
                email=email,
                platform="Website",
                message=message,
                status="new"
            )
            db.session.add(contact_message)
            db.session.commit()

            flash("Your message has been sent successfully.", "success")
        except Exception as e:
            flash("Something went wrong. Please try again later.", "danger")
            print(f"Error: {e}")

        return redirect(url_for('contact'))
    
    return render_template('messages/contact.html')


# --------------- Admin Dashboard Route ---------------
@app.route('/admin_dashboard')
@login_required
@admin_required
def admin_dashboard():
    total_projects = Project.query.count()
    total_skills = Skill.query.count()
    total_testimonials = Testimonial.query.count()
    total_messages = ContactMessage.query.count()
    unread_messages = ContactMessage.query.filter_by(status='new').count()
    responded_messages = ContactMessage.query.filter_by(status='responded').count()

    return render_template('dashboard/admin_dashboard.html', 
                           total_projects=total_projects, 
                           total_skills=total_skills, 
                           total_testimonials=total_testimonials, 
                           total_messages=total_messages, 
                           unread_messages=unread_messages, 
                           responded_messages=responded_messages)


if __name__ == "__main__":
    app.run(debug=True, port=8000)