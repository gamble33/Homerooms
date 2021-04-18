from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

database = SQLAlchemy()
DB_NAME = "database.database"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'j4857zk392956f'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    database.init_app(app)

    from website.views.views import views
    from website.views.auth import auth
    from website.views.school import school
    from website.views.election import election

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')
    app.register_blueprint(school, url_prefix='/school/')
    app.register_blueprint(election, url_prefix='/election/')

    # Importing models the run initialise classes before database is created
    from .models.User import User, Student, Teacher
    from .models.School import School
    from .models.Election import  Election, Candidate

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
        database.create_all(app=app)
        print("Created Database!")
