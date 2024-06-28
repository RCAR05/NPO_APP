from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)
# [RC Notes:]@auth.route(‘/sign-up’) defined the URL that this sign-up page would be at. 
# For the method needed for this function we would need both a POST (the user giving information) and 
# GET (retrieving information). First we want to define the variables that the form. 
# This action is done with the get method. 
# Next we validate the data from the form. 
# The first and most important validation is the email, here we ensure that the email is not duplicated. 
# We also check other factors like length of strings to ensure that the account is not empty, and the password is confirmed.
@auth.route('/sign-up', methods= ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # define variables based on form inputs
        userType = request.form.get('userType')
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        schoolName = request.form.get('schoolName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        validate_user = False
        # validate each input based on silly product manager specs
        # [RC Note:] TODO: persist user data on form when validation fails. This is necessary because it is frustrating to have
        # to redo all the questions because you submitted too early or did something to get an error. 
        if user and validate_user: 
            flash('Email exists already', category='error')
        elif len(userType)<1 and validate_user:
            flash('Please enter either student or organization.', category='error')  
        elif len(email) < 4 and validate_user:
            flash('Email is not valid.', category='error')
        elif len(first_name) <2 and validate_user:
            flash('Name is too short, needs to more than 1 characters.', category='error')
        elif len(schoolName) <5 and validate_user:
            flash('School or Organization name is too short, needs to more than 4 characters.', category='error')
        elif password1 != password2 and validate_user:
            flash('Passwords do not match.', category='error')
        elif len(password1) <7 and validate_user:
            flash('Password is too short, needs to be at least 7 characters', category='error')
        else: 
            new_user = User(userType=userType, email= email, first_name=first_name, password=generate_password_hash(
                # [RC Note:] The one challenge with the password that I encountered was that because I was using reference 
                # material that was a few years old, the initial hash method was simply sha256 but this was not working. 
                # After some research I found out that it needed to be updated to pbkdf:sha256 for the method to work. 
                # This was an example of needing to do the steps slowly and checking every few steps so that errors could be 
                # identified early and handled individually. ]
                password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account Created!', category='success')
            return redirect(url_for('views.home')) 
        # If valid, add to DB
    return render_template("sign_up.html", user=current_user)
# [RC Notes:] For the sign up.html I initially set up two pages, one for students and one for organization. 
# Eventually I realized that they were very similar and so I combined them into one but used a drop down for the 
# student or organization choice to ensure that the form wouldn’t have free text errors that would interfer with later 
# work flows like if user is a student in the base html which defined which pages they could use. 
@auth.route('/login', methods= ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

