from flask import Blueprint, render_template, current_app, redirect, url_for, request, flash
from flask_login import current_user, login_required

from website import database

from website.models.User import Student, User
from website.models.Election import Election, Candidate
from website.models.School import School

election = Blueprint('election', __name__)


@election.route('/', methods=['GET'])
@login_required
def home():
    if not current_user.school_id:
        return redirect(url_for('school.create_school'))

    return render_template("school/school_create_election.html", user=current_user)


@election.route('/create-election', methods=['GET', 'POST'])
@login_required
def create_election():
    if not current_user.school_id:
        return redirect(url_for('school.create_school'))

    if request.method == 'POST':
        election_title = request.form.get('title')
        student_amount = int(request.form.get('student-amount'))
        candidate_amount = int(request.form.get('candidate-amount'))

        if student_amount < 2:
            flash("You must have at least 2 voting students to create an election", category='error')
        elif candidate_amount < 2:
            flash("There must be at least 2 candidates in an election", category='error')

        # All requirements are met and an election can be created
        else:
            new_election = Election(title=election_title, school_id=current_user.school_id,
                                    student_amount=student_amount,
                                    candidate_amount=candidate_amount)

            database.session.add(new_election)
            database.session.commit()

    return render_template("school/school_create_election.html", user=current_user)


@election.route('/see-elections', methods=['GET'])
@login_required
def see_elections():

    if not current_user.school_id:
        return redirect(url_for('school.create_school'))

    school = School.query.filter_by(id=current_user.school_id).first()
    """
    School of current user
    """

    elections = Election.query.filter_by(school_id=current_user.school_id)
    """
    Array of all elections within the users school
    """

    return render_template("school/school_election_list.html", user=current_user, school=school, elections=elections)
