from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Testimonial, StudentProfile, OrgProfile
from . import db
import json
from .utils import get_ai_project

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)

#This is intended to use some of the notes functionality but without the delete button. Going to copy and paste the above code from notes. 
@views.route('/testimonials', methods=['GET', 'POST'])
def testimonial():
    if request.method == 'POST': 
        testimonial = request.form.get('testimonial')#Gets the note from the HTML 

        if len(testimonial) < 1:
            flash('Testimonial is too short!', category='error') 
        else:
            new_testimonial = Testimonial(data=testimonial, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_testimonial) #adding the note to the database 
            db.session.commit()
            flash('Testimonial added!', category='success')

    all_testimonials = Testimonial.query.all()

    return render_template("testimonials.html", user=current_user, testimonials=all_testimonials)

#Student Profile getting variables from the form and committing to database
@views.route('/profile', methods =['GET', 'POST'])
@login_required
def student_profile():
    #user_data = StudentProfile.query()

    if request.method == 'POST':
        #Get form variables
        education = request.form.get('education_level')
        major = request.form.get('education_major')
        skills = request.form.get('skills')
        work = request.form.get('work_experience')
        interests = request.form.get('interests')
        hours = request.form.get('available_hours')
        email = request.form.get('email')
        ai_enhancement = request.form.get('ai_profile_enhancement')
        #Validate form variables
        if len(education) < 1:
            flash("Education level required", category='error')
        elif len(work) < 1:
            flash("Work experience required", category='error')
        elif len(hours) < 1:
            flash("Available hours required", category='error')
        else: 
            #add to database
            new_student_profile = StudentProfile(
                education_level=education,
                education_major=major,
                skills=skills,
                work_experience=work,
                interests=interests,
                hours=hours,
                email=email,
                user_id=current_user.id,
            )
            db.session.add(new_student_profile) #adding the note to the database 
            db.session.commit()
            #Flash confirmation
            flash('Congratulations! Profile created!', category='success')
    return render_template("student_profile.html", user=current_user)

    


#Organizational Profile getting variables from the form and committing to database
@views.route('/org_profile', methods =['GET', 'POST'])
@login_required
def org_profile():
    if request.method == 'POST':
        #Get form variables
        description = request.form.get('org_description')
        mission = request.form.get('mission')
        project = request.form.get('project_desc')
        goals = request.form.get('goals')
        required_skills = request.form.get('required_skills')
        org_hours = request.form.get('estimated_hours')
        email = request.form.get('email')
        ai_enhancement = request.form.get('ai_project_enhancement')
        #Validate form variables
        if len(description) < 1:
            flash("Description of the organization required", category='error')
        elif len(project) < 1:
            flash("Description of the project required", category='error')
        elif len(org_hours) < 1:
            flash("Estimated hours required", category='error')
        else: 
            # generate ai description
            if ai_enhancement == "True":
                ai_project = get_ai_project(human_project_desc=project)
            else:
                ai_project = ""
            #add to database
            new_org_profile = OrgProfile(
                org_description=description,
                mission=mission,
                project_desc=project,
                ai_project_desc=ai_project,
                goals=goals,
                required_skills=required_skills,
                estimated_hours=org_hours,
                email=email,
                user_id=current_user.id,
            )
            db.session.add(new_org_profile) #adding the org profile to the database 
            db.session.commit()
            #Flash confirmation
            flash('Congratulations! Organizational Profile created!', category='success')
    return render_template("organization_profile.html", user=current_user)
#Data pull for the tables
#headings = ("Organization", "Project Description", "Estimated Hours")
#[RC Note:] the two views below were required to share the information that each user had shared in the user registration. 
# For this we would query the database for each user. 
@views.route('/projects', methods=['GET'])
@login_required
def projects():
    projects = OrgProfile.query.all()
    return render_template("projects.html", user=current_user, projects=projects)

@views.route('/prospects', methods=['GET'])
@login_required
def prospects():
    # NOTE: not all student users have student profiles
    prospects = StudentProfile.query.all()
    return render_template("prospects.html", user=current_user, prospects=prospects)
    
##This will not be required in the final version
@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})