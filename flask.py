from flask import Flask, render_template, request, redirect, url_for

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_type = request.form['user_type']
        name = request.form['name']
        email = request.form['email']
        skills = request.form.get('skills')
        projects = request.form.get('projects')
        # Store this information in a database or Google Sheets
        return redirect(url_for('index'))
    return render_template('register.html')

import gspread
from google.oauth2.service_account import Credentials

# Set up Google Sheets API
scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credentials = Credentials.from_service_account_file('path_to_credentials.json', scopes=scopes)
client = gspread.authorize(credentials)
sheet = client.open('NonProfit_Student_Connection').sheet1

@app.route('/register', methods=['POST'])
def register():
    user_type = request.form['user_type']
    name = request.form['name']
    email = request.form['email']
    skills = request.form.get('skills')
    projects = request.form.get('projects')

    if user_type == 'student':
        sheet.append_row([name, email, skills, ''])
    else:
        sheet.append_row([name, email, '', projects])

    return redirect(url_for('index'))

