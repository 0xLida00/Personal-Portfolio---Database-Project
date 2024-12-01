from datetime import datetime, timezone
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(75), unique=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    role = db.Column(db.String(10), default='visitor', nullable=False)
    active = db.Column(db.Boolean, default=True)  # Active status for user
    password = db.Column(db.String(128)) # Store plain text password (I WILL NOT USE this approach in real life but just for this project and academic reasons - we will be learning better approaches in the next module)

    projects = db.relationship('Project', back_populates='user')
    skills = db.relationship('Skill', back_populates='user')
    experiences = db.relationship('Experience', back_populates='user')
    testimonials = db.relationship('Testimonial', back_populates='user')
    contact_messages = db.relationship('ContactMessage', back_populates='user')
    external_users = db.relationship('ExternalUser', back_populates='user')

    def __repr__(self):
        """Return a string representation of the user object."""
        return f"<User {self.username}> has {self.role} role and {self.email} as email"
        
    def is_admin(self):
        """Return True if the user is an admin."""
        return self.role == 'admin'
    
    def get_id(self):
        """Return the user ID as a string."""
        return str(self.user_id)
    
    def set_password(self, password):
        """Set the password hash for the user."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check if the password is correct."""
        return check_password_hash(self.password, password)


class ExternalUser(db.Model):
    __tablename__ = 'external_users'

    external_user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(75), nullable=False, unique=True)
    platform = db.Column(db.String(50), nullable=False)  # e.g., "Website", "LinkedIn"
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)  # Link to an authenticated user if needed

    user = db.relationship('User', back_populates='external_users')
    testimonials = db.relationship('Testimonial', back_populates='external_user')
    contact_messages = db.relationship('ContactMessage', back_populates='external_user')

    def __repr__(self):
        """Return a string representation of the external user object."""
        full_name = f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.first_name or self.last_name
        return f"<ExternalUser {full_name}> from {self.platform}, joined at {self.created_at}"


class Project(db.Model):
    __tablename__ = 'projects'

    project_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.String(255))
    link = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', back_populates='projects')

    def __repr__(self):
        """Return a string representation of the project object."""
        return f"User {self.user.username} manages <Project {self.title}> which is about '{self.description}'"
    

class Skill(db.Model):
    __tablename__ = 'skills'

    skill_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False)
    proficiency_level = db.Column(db.String(50))
    category = db.Column(db.String(50))
    active = db.Column(db.Boolean, default=True)

    user = db.relationship('User', back_populates='skills')

    def __repr__(self):
        """Return a string representation of the skill object."""
        return f"user_id {self.user_id} has <Skill {self.skill_name}> skill with {self.proficiency_level} proficiency level"


class Experience(db.Model):
    __tablename__ = 'experiences'

    experience_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    description = db.Column(db.Text, nullable=False)

    user = db.relationship('User', back_populates='experiences')

    def __repr__(self):
        """Return a string representation of the experience object."""
        return f"user_id {self.user_id} possesses <Experience {self.position} at {self.company}>"


class Testimonial(db.Model):
    __tablename__ = 'testimonials'

    testimonial_id = db.Column(db.Integer, primary_key=True)
    external_user_id = db.Column(db.Integer, db.ForeignKey('external_users.external_user_id', ondelete="CASCADE"), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    platform = db.Column(db.String(50))
    is_responded = db.Column(db.Boolean, default=False)
    response = db.Column(db.Text)
    response_created_at = db.Column(db.DateTime)

    external_user = db.relationship('ExternalUser', back_populates='testimonials')
    user = db.relationship('User', back_populates='testimonials')

    def __repr__(self):
        """Return a string representation of the testimonial object."""
        return f"user_id {self.user_id} received <Testimonial by {self.author_name} from {self.platform} at {self.created_at}>"


class ContactMessage(db.Model):
    __tablename__ = 'contactmessages'

    message_id = db.Column(db.Integer, primary_key=True)
    external_user_id = db.Column(db.Integer, db.ForeignKey('external_users.external_user_id', ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete="CASCADE"), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(75), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(20), nullable=False, default='new', index=True)
    response = db.Column(db.Text)
    response_created_at = db.Column(db.DateTime)

    external_user = db.relationship('ExternalUser', back_populates='contact_messages')
    user = db.relationship('User', back_populates='contact_messages')
    message_threads = db.relationship('MessageThread', foreign_keys='MessageThread.message_id', back_populates='contact_message')

    def __repr__(self):
        """Return a string representation of the contact message object."""
        return f"user_id {self.user_id} received <ContactMessage from External User {self.external_user_id} at {self.created_at}>: '{self.message}'"


class MessageThread(db.Model):
    __tablename__ = 'messagethreads'
    
    thread_id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('contactmessages.message_id', ondelete="CASCADE"), nullable=False)
    reply_id = db.Column(db.Integer, db.ForeignKey('contactmessages.message_id', ondelete="CASCADE"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    contact_message = db.relationship('ContactMessage', foreign_keys=[message_id], back_populates='message_threads')
    reply_message = db.relationship('ContactMessage', foreign_keys=[reply_id])

    def __repr__(self):
        """Return a string representation of the message thread object."""
        return f"<MessageThread {self.thread_id} with message_id {self.message_id} and reply_id {self.reply_id} created at {self.created_at}>"