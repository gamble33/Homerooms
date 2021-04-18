from flask import Blueprint, render_template, current_app, redirect, url_for, request, flash
from flask_login import current_user, login_required

from website import database

from website.models.User import Student, User
from website.models.Election import Election, Candidate

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
        student_amount = request.form.get('student-amount')
        candidate_amount = request.form.get('candidate-amount')

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
