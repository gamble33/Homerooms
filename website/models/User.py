from .. import database
from flask_login import UserMixin
from sqlalchemy import func


def create_student(user_id):
    data = "Test data"
    new_student = Student(data=data, user_id=user_id)
    database.session.add(new_student)
    database.session.commit()
    print('Student Created!')


# TODO: add constraints for relationship (foreign key)
class User(database.Model, UserMixin):
    """
    User model class \n
    (id(auto), email, password, date_created(auto), is_admin)
    """

    id: int = database.Column(database.Integer, primary_key=True)
    """
    Primary key (integer id)
    """

    name: str = database.Column(database.String(150))
    """
    Name of the user
    """

    email: str = database.Column(database.String(150), unique=True)
    """
    Unique email (str, max 150 chars)
    """

    password: str = database.Column(database.String(150))
    """
    Password (hashed) (str, max 150 chars)
    """

    date_created = database.Column(database.DateTime(timezone=True), default=func.now())
    """
    Date that user account was created
    """

    school_id = database.Column(database.Integer, database.ForeignKey('school.id'))
    """
    Foreign key id of the school of this user (default: NONE)
    """

    is_admin: bool = database.Column(database.Boolean)
    """
    Is the user and admin (boolean)
    """

    is_teacher: bool = database.Column(database.Boolean)
    """
    Is the user a teacher (admin)
    """


class Teacher(database.Model):
    """
    Teacher class \n
    id (primary key)) \n
    user_id (foreign key, 'user.id') \n
    """

    id: int = database.Column(database.Integer, primary_key=True)

    # Todo: Get rid of this shit
    data: str = database.Column(database.String(150))

    user_id: int = database.Column(database.Integer, database.ForeignKey('user.id'))


class Student(database.Model):
    id: int = database.Column(database.Integer, primary_key=True)

    user_id = database.Column(database.Integer, database.ForeignKey('user.id'))

    data: str = database.Column(database.String(150))
