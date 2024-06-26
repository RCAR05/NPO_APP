from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class StudentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    education_level = db.Column(db.String(1000))
    education_major = db.Column(db.String(1000))
    skills = db.Column(db.String(1000))
    work_experience = db.Column(db.String(1000))
    interests = db.Column(db.String(1000))
    hours = db.Column(db.String(100))
    email = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class OrgProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    org_description = db.Column(db.String(1000))
    mission = db.Column(db.String(1000))
    project_desc = db.Column(db.String(1000))
    ai_project_desc = db.Column(db.String(1000), default="")
    goals = db.Column(db.String(1000))
    required_skills = db.Column(db.String(1000))
    estimated_hours = db.Column(db.String(100))
    email = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    userType = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    school_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    testimonials = db.relationship('Testimonial')
    student_profile = db.relationship('StudentProfile')

    @property
    def is_student(self):
        return self.userType == "Student"



