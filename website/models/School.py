from .. import database
from flask_login import UserMixin
from sqlalchemy import func


class School(database.Model):
    id: int = database.Column(database.Integer, primary_key=True)

    users = database.relationship('User')
    """
    Database relationship contains references to all users of this school
    """