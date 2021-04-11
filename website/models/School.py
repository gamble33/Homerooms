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