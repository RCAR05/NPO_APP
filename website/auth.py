from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

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
        # TODO: persist user data on form when validation fails
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
                password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account Created!', category='success')
            return redirect(url_for('views.home')) 
        # If valid, add to DB
    return render_template("sign_up.html", user=current_user)

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

