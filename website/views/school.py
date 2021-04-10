from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user

from website import database
from website.models.User import Teacher

school = Blueprint('school', __name__)


def checkUserTeacher():
    """
    Checks and returns if the current user is a teacher (Redirects user to 'views.home' if they are not a teacher
    :return: Boolean (True - current_user teacher, False - current_user not teacher)
    """

    if current_user.is_teacher:
        return True

    return False


@school.route('/', methods=['GET'])
def school_home():

    # TODO: Figure out how to not copy paste this code
    if not checkUserTeacher():
        return redirect(url_for('views.home'))

    teacher = Teacher.query.filter_by(id=current_user.id).first()
    print(teacher)

    return redirect(url_for('school.create_school'))


@school.route('/create-school', methods=['GET', 'POST'])
def create_school():

    if not checkUserTeacher():
        return redirect(url_for('views.home'))

    if current_user.school_id:
        print("Has school Id")
    else:
        print("No school id")

    if request.method == 'POST':
        school_name = request.form.get('name')




    return render_template("create_school.html", user=current_user)
