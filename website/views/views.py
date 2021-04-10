from flask import Blueprint, render_template, current_app
from flask_login import current_user

from website.models.User import Student, User

views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def home():

    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()

    users_list = User.query.all()

    return render_template("home.html", user=current_user, users_list=users_list)
