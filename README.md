# Personal-Portfolio---Database-Project

## Overview

This project is a **Personal Portfolio Website** that showcases your skills, projects, and experiences. It includes a **Project Management** section where you can manage your portfolio's projects and receive feedback from external users. The app also features a **contact form** and handles testimonials submitted by external users, all while providing a clean and modular structure.

---

## User Story

### **As a user (admin), I want to manage my portfolio website to showcase my projects, skills, and experiences so that I can demonstrate my professional expertise and make my portfolio interactive and engaging.**

**Acceptance Criteria:**

1. **User Authentication:**
   - Users can sign up, log in, and manage their own profiles securely.
   - Admin users can log in and access administrative tools to manage projects, skills, and experiences.

2. **Project Management:**
   - Admins can add, edit, and delete projects.
   - Projects include details like title, description, technologies used, and links to the project.
   - Admins can view a list of all projects in a dedicated page.

3. **Skill and Experience Management:**
   - Admins can add, edit, and delete skills and experiences.
   - The skills page lists the user's skills along with proficiency levels.
   - The experience page lists work experiences with detailed job descriptions.

4. **External User Interaction:**
   - External users can leave testimonials about the user's work.
   - Admins can view, reply to, and manage testimonials.
   - External users can send messages through a contact form, and admins can reply to these messages.
   - Message threads can be created for ongoing communication with external users.

5. **Design and Responsiveness:**
   - The website is built with modern design practices, ensuring a clean, responsive, and user-friendly experience.
   - The website is designed with accessibility in mind (color contrast, legible fonts).

---
**Features:**
   - User Authentication: Admin can log in and manage their portfolio.
   - Project Management: Add, edit, and delete projects
   - Skills & Experience Management: Manage skills and professional experience.
   - Testimonials: External users can submit testimonials, and admins can respond to them.
   - Contact Messages: External users can send messages through the contact form.
   - Message Threads: Admins can respond to messages and maintain a thread for communication.

**Future Enhancements:**
   - Admin Dashboard: Build an interactive dashboard for easier project management.
   - Analytics: Add an analytics page to track user engagement or testimonials.
   - Interactions: Add instant chat widget to interact with users and Partners in real time.
   - Expand to Public: Allow Users to create and administrate their own portfolio.

**Entity-Relationship Diagram (ERD) and Database Structure:**
    The entities, relationships, and the corresponding Entity-Relationship Diagram (ERD) for the project are detailed in a separate document. You can view and download the document [here](docs/Personal_Portfolio_Website_with_Project_Management.pdf).
    This document provides an in-depth overview of the database schema and how the entities relate to each other in the context of the application.

## Setup Instructions

Follow the steps below to set up and run the project locally.

### Prerequisites

Make sure you have the following installed:
- Python 3.7+
- pip (Python package manager)

### 1. Clone the Repository
        ```bash
        git clone https://github.com/0xLida00/Personal-Portfolio---Database-Project.git
        cd Personal-Portfolio---Database-Projec

    2. Install Dependencies
        Create a virtual environment and activate it:
        python3 -m venv venv
        source venv/bin/activate  # For macOS/Linux
        venv\Scripts\activate     # For Windows

    Install the necessary dependencies:
        pip install -r [requirements.txt](http://_vscodecontentref_/0)

    3. Set Up Database
    The app uses Flask-SQLAlchemy for database management. Initialize the database by running the migration commands:
    This ensures that each code block is properly formatted and separated from the text.
        flask db init
        flask db migrate -m "Initial migration"
        flask db upgrade
    This will set up the required tables in your database.

    4. Configure the App
    Make sure to configure the app’s settings (such as database URI and secret key) in config.py or directly in the app.

    5. Run the Application
    To run the app locally, use the following command:
        flask run
    The application will be available at http://127.0.0.1:8000.


Structure :
Directory Layout
```
Personal-Portfolio--Database-Project/
    |── app.py
    |── static/
    |     |── css/
    |     |    |── styles.css
    |     |── js/
    |     |    |── scripts.js
    |── templates/
    |     |── auth/
    |     |    |── login.html
    |     |    |── register.html
    |     |── dashboard/
    |     |    |── admin_dashboard.html
    |     |    |── manage_experiences.html
    |     |    |── manage_projects.html
    |     |    |── manage_skills.html
    |     |    |── user_management.html
    |     |── messages/
    |     |    |── contact.html
    |     |    |── message_detail.html
    |     |    |── messages.html
    |     |── portfolio/
    |     |    |── experiences.html
    |     |    |── projects.html
    |     |    |── skills.html
    |     |── base.html
    |     |── index.html
    |── config.py
    |── models.py
    |── requirements.txt
    |── README.md
    |── sandbox.ipynb
    |── .gitignore
    |── venv/


	•	models.py: Contains the model definitions (e.g., User, Project, Testimonial).
	•	templates: Contains HTML templates.
	•	static: Contains static assets like CSS and JavaScript files.
	•	app.py: The core Flask application file where the app is initialized and Flask routes are defined to handle requests and responses.

