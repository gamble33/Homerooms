from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user, login_user, logout_user

import json

from werkzeug.security import generate_password_hash, check_password_hash
# Password hashing and checking library

from website import database
from website.models.User import User, Student, Teacher
from website.models.School import School

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login route for all users (students/teachers/admins) \n
    :return: Returns login page (for get request) and redirects to home page on login
    """

    if current_user.is_authenticated:
        return render_template("error_pages/already_logged_in.html", user=current_user)

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        remember_user = request.form.get('remember-me') == 'on'
        """
        If the user login will be remembered or not
        """

        user = User.query.filter_by(email=email).first()

        # Checks if email of user exists in database
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=remember_user)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('This user does not exist (check email spelling)', category='error')

    return render_template("login.html", user=current_user)


def validate_sign_up(email, password, confirm_password):
    """
    Validates a user submitted sign up form
    :param email: Email of the user from from data
    :param password: Password of user from form data
    :param confirm_password: (Repeat/Confirm) Password of user from form data
    :return: Returns True - if all data is valid, False - if the account creation is invalid
    """

    existing_user = User.query.filter_by(email=email).first()
    """
    Searches data base and checks if user email is already registered
    """

    # If user already exists in database
    if existing_user:
        flash('Email is already registered', category='error')

    # Check that user typed in an email
    elif len(email) < 1:
        flash('Email field must not be empty', category='error')

    # Checks that password is at least 7 characters
    elif len(password) < 7:
        flash('Password must be at least 7 characters long', category='error')

    # Checks that user entered password and 'confirm password' are equal
    elif password != confirm_password:
        flash('Passwords must match', category='error')

    # All conditions were met and new user is created and added to database
    else:

        # Adding user to database
        return True

    # Some test case failed and user account is invalid (invalidation)
    return False


def create_user(new_user, remember_user):
    """
    Sumbits the new_user object to the database and commits the session, then redirects user to home page
    :param new_user: The new User object that was created
    :param remember_user: If the user should be remembered on login or not (Remember Me [ ] check box)
    """

    database.session.add(new_user)
    database.session.commit()

    flash('New Account Created!', category='success')
    login_user(new_user, remember=remember_user)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """
    Sign up route for student accounts (Not teachers)
    :return: Returns sign up page (on get requests), logs in automatically on account creation (and redirects to home page)
    """

    if current_user.is_authenticated:
        return render_template("error_pages/already_logged_in.html", user=current_user)

    if request.method == 'POST':

        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        school_id = request.form.get('school-id')

        remember_user = request.form.get('remember-me') == 'on'
        """ If the user should be remembered after login or not """

        is_admin = False

        # Validate School Code
        school = School.query.filter_by(id=school_id).first()

        # Sign up was validated and account can be created
        if validate_sign_up(email, password, confirm_password):

            # For checking If the code of school that student entered doesn't exist
            if school:

                # For checking If the code of school that student entered doesn't exist
                # Creates new Student Object
                hashed_password = generate_password_hash(password, method='sha256')
                new_user = User(name=name, email=email, password=hashed_password, is_teacher=False, school_id=school_id)

                # Submits Student Object to database
                create_user(new_user, remember_user)

                # Creates student instance (Student instance and user instance have the same primary keys
                new_student = Student(data='Students are fat', user_id=new_user.id)

                database.session.add(new_student)
                database.session.commit()

                return redirect(url_for('views.home'))

            # School doesn't exist (School code entered is not valid)
            else:
                flash('School code is not valid', category='error')

    return render_template("sign_up.html", user=current_user)


@auth.route('/sign-up-teacher', methods=['GET', 'POST'])
def sign_up_teacher():
    if current_user.is_authenticated:
        return render_template("error_pages/already_logged_in.html", user=current_user)

    if request.method == 'POST':

        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        remember_user = request.form.get('remember-me') == 'on'
        """ If the user should be remembered after login or not """

        is_admin = False

        # Sign up was validated and account can be created
        if validate_sign_up(email, password, confirm_password):
            # Creates new Teacher Object
            hashed_password = generate_password_hash(password, method='sha256')
            new_user = User(name=name, email=email, password=hashed_password, is_admin=is_admin, is_teacher=True)

            # Submits User Object to database
            create_user(new_user, remember_user)

            # Create teacher object (User & Teachers instances have the same primary key)
            new_teacher = Teacher(data='teachers are fat', user_id=new_user.id)

            database.session.add(new_teacher)
            database.session.commit()

            return redirect(url_for('views.home'))

    return render_template("sign_up_teacher.html", user=current_user)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    """
    Default logout route for all logged-in users
    :return: Redirects user to login page on logout event
    """

    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/delete-user', methods=['POST'])
def delete_user():
    user = json.loads(request.data)
    user_id = user['userId']
    user = User.query.get(user_id)

    if user:

        is_teacher = user.is_teacher
        id = user.id

        database.session.delete(user)
        database.session.commit()

        if is_teacher:
            database.session.delete(Teacher.query.get(id))
        else:
            database.session.delete(Student.query.get(id))

    return jsonify({})
