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