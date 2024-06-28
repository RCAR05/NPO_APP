from flask import Flask
from flask_sqlalchemy import SQLAlchemy as sqlal
from os import path
from flask_login import LoginManager

# [RC Notes:] __Init__.py this was the file that sat with in the website folder. This allowed the website folder to viewed as a package. 
# And allowing you to import from the website package.  
# In this file we imported Flask which is a web framework for python, that makes it easy to get started with web development. 
# Perfect for this type of project. The most useful thing is that it makes it very easy to test and debug the code as you progress. 
# It also integrates with Jinja2 which helps in generating HTML form templates. 
# It also has extensions that help handle user authentication (Flask_Login) and, form handling and database integration 
# (Flask_SQLALCHEMY) which are all aspects we had identified as necessary for our project. 

db = sqlal()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'takeover'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User


    with app.app_context():
        create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        # db.create_all(app=app)
        db.create_all()
        print('Created Database!')