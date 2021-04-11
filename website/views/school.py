from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required

from website import database
from website.models.User import Teacher, Student, User
from website.models.School import School, Homeroom

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

    _school = School.query.filter_by(id=current_user.school_id).first()

    # If the current user (teacher) is a part of school
    if current_user.school_id:
        return render_template("school_home.html", user=current_user, school=_school)

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


@school.route('/see-students', methods=['GET'])
@login_required
def see_students():
    """
    List of all students in a school
    :return:
    """

    # Is user a part of the school?
    if not current_user.school_id:
        return redirect(url_for('school.create_school'))

    _school = School.query.filter_by(id=current_user.school_id).first()

    student_user = {}

    users = User.query.filter_by(school_id=_school.id, is_teacher=False)
    """
    List of all users in the same school as the current user (current teacher)
    """

    for user in users:
        student_user[user] = Student.query.get(user.id)

    return render_template("school_students_list.html", user=current_user, users=users, school=_school,
                           student_user=student_user)


@school.route('/see-homerooms', methods=['GET'])
@login_required
def see_homerooms():
    """
    List of all homerooms in a school
    :return:
    """

    if not current_user.school_id:
        return redirect(url_for('school.create_school'))

    _school = School.query.filter_by(id=current_user.school_id).first()

    homerooms = Homeroom.query.filter_by(school_id=_school.id)

    return render_template("school_homerooms_list.html", user=current_user, homerooms=homerooms, school=_school)


@school.route('/create-homeroom', methods=['GET', 'POST'])
@login_required
def create_homeroom():
    """
    Create and register a homeroom instance to the database
    :return:
    """

    if not current_user.school_id:
        return redirect(url_for('school.create_school'))

    _school = School.query.filter_by(id=current_user.school_id).first()

    if request.method == 'POST':
        homeroom_name = request.form.get('name')

        new_homeroom = Homeroom(name=homeroom_name, school_id=_school.id)

        database.session.add(new_homeroom)
        database.session.commit()

        return redirect(url_for('school.see_homerooms'))

    return render_template("school_create_homeroom.html", user=current_user)