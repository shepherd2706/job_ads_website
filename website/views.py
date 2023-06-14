'''
Zawiera URL do komponentow strony
'''

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Job, User
from . import db
import json
from sqlalchemy.sql import select

views = Blueprint(name='views', import_name=__name__)

# to co w home odpali sie gdy wejde w URL tego konkretnego widoku
@views.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        pos = request.form.get('position')
        desc = request.form.get('description') # dane z forma o name=description
        sal = request.form.get('salary') # request.form jest slownikiem pythonowym dlatego uzywamy metody get()
        loc = request.form.get('localisation')
        if len(pos) < 1:
            flash('Position cannot be empty!', category='error')
        elif len(sal) < 1:
            flash('Salary cannot be empty!', category='error')
        elif len(desc) < 1:
            flash('Localisation cannot be empty!', category='error')
        elif len(loc) < 1:
            flash('Description cannot be empty!', category='error')
        else:
            new_job = Job(user_id=current_user.id, salary=sal, description=desc, localisation=loc, position=pos)
            db.session.add(new_job)
            db.session.commit()
            flash('Added!', category='success')

    return render_template('account.html', user=current_user) # funkcja zwraca template z pliku home.html

@views.route('/delete-job', methods=['POST'])
def delete_job():
    job = json.loads(request.data) # funkcja dostaje plik json z index.js
    job_id = job['jobId']
    job = Job.query.get(job_id)
    if job:
        if job.user_id == current_user.id:
            db.session.delete(job)
            db.session.commit()

    return jsonify({})

@views.route('/', methods=['GET', 'POST'])
def home():
    jobs = Job.query.all()
    users = User.query.all()
    positions = Job.query.with_entities(Job.position).distinct().order_by(Job.position.asc()).all()
    if request.method == 'POST':
        filter_position = request.form.get('filter_position', '')
        filtered_jobs = Job.query.filter(
            (Job.position == filter_position if filter_position else True)
        ).all()

        return render_template('home.html', positions=positions, user=current_user, jobs_data=filtered_jobs, users_data=users, filter_position=filter_position)

    return render_template('home.html', positions=positions, user=current_user, jobs_data=jobs, users_data=users)

    # return render_template('home.html', user=current_user, jobs_data=jobs, users_data=users)
