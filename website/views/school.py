from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required

from website import database
from website.models.User import Teacher
from website.models.School import School

school = Blueprint('school', __name__)


def checkUserTeacher():
    """
    Checks and returns if the current user is a teacher (Redirects user to 'views.home' if they are not a teacher
    :return: Boolean (True - current_user teacher, False - current_user not teacher)
    """

    if current_user.is_teacher:
        return True

    return False


def register_school(school_name):
    """
    Adds school to a database
    :param school_name: The name of the school
    """

    new_school = School(name=school_name)

    database.session.add(new_school)
    database.session.commit()

    current_user.school_id = new_school.id

    database.session.commit()


@school.route('/', methods=['GET'])
@login_required
def school_home():
    # TODO: Figure out how to not copy paste this code
    if not checkUserTeacher():
        return redirect(url_for('views.home'))

    teacher = Teacher.query.filter_by(id=current_user.id).first()
    print(teacher)

    # If the current user (teacher) is a part of school
    if current_user.school_id:
        return render_template("school_home.html", user=current_user)

    return redirect(url_for('school.create_school'))


@school.route('/create-school', methods=['GET', 'POST'])
@login_required
def create_school():
    if not checkUserTeacher():
        return redirect(url_for('views.home'))

    # Is a part of a school
    if current_user.school_id:
        return redirect(url_for('school.school_home'))

    if request.method == 'POST':
        school_name = request.form.get('name')
        register_school(school_name)
        return redirect(url_for('school.school_home'))

    return render_template("create_school.html", user=current_user)
