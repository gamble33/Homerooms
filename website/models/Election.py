from .. import database
from flask_login import UserMixin
from sqlalchemy import func


class Election(database.Model):
    """
    Students vote for 1 of multiple candidates and the election ends in one of two cases \n
    1) A winning candidate is chosen. \n
    2) There is a tie between multiple candidates, and the election can be re-run with the winning candidates \n
    \n

    id - unique id of the election \n
    candidate_amount - the amount of candidates in election \n
    student_amount - the amount of students in election \n
    title - the title of the election \n
    school_id - foreign key, of the school of this election \n
    """

    id: int = database.Column(database.Integer, primary_key=True)

    candidate_amount: int = database.Column(database.Integer)
    """
    The amount of candidates participating in this election
    """

    student_amount: int = database.Column(database.Integer)
    """
    The amount of students participating in this election
    """

    title: str = database.Column(database.String(300))
    """
    The title of the election, example ('The School Vice President Election')
    """

    school_id = database.Column(database.Integer, database.ForeignKey('school.id'))


class Candidate(database.Model):
    id: int = database.Column(database.Integer, primary_key=True)

    user_id = database.Column(database.Integer, database.ForeignKey('user.id'))

    bio: str = database.Column(database.String(5000))
    """
    Any text that the candidate wants to be publicly displayed during voting
    """

    election_id = database.Column(database.Integer, database.ForeignKey('election.id'))
