from .. import database
from flask_login import UserMixin
from sqlalchemy import func


class School(database.Model):
    id: int = database.Column(database.Integer, primary_key=True)

    name: str = database.Column(database.String(150))
    """
    The name of the school (example 'International School of Nice')
    """

    users = database.relationship('User')
    """
    Database relationship contains references to all users of this school
    """


class Homeroom(database.Model):
    """
    Homeroom / Tutor group, contains a set of students \n
    id - primary key \n
    name - name of homeroom (e.g. '10C') \n
    students - database relationship to 'Student' \n
    school_id - the id of the school that homeroom is a part of \n
    """

    id: int = database.Column(database.Integer, primary_key=True)

    name: str = database.Column(database.String(150))
    """
    The name of the homeroom / Tutor Group (E.g. '7A')
    """

    students = database.relationship('Student')
    """
    Database relationship contains references to all users of this school
    """

    school_id = database.Column(database.Integer, database.ForeignKey('school.id'))
    """
    Id of the school that this homerooms is a part of
    """