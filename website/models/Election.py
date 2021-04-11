from .. import database
from flask_login import UserMixin
from sqlalchemy import func


class Candidate(database.Model):
    id: int = database.Column(database.Integer, primary_key=True)

    user_id = database.Column(database.Integer, database.ForeignKey('user.id'))

    bio: str = database.Column(database.String(5000))
    """
    Any text that the candidate wants to be publicly displayed during voting
    """
