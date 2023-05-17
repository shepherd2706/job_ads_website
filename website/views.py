'''
Zawiera URL do komponentow strony
'''

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Job
from . import db
import json

views = Blueprint(name='views', import_name=__name__)

# to co w home odpali sie gdy wejde w URL tego konkretnego widoku
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        desc = request.form.get('description') # dane z forma o name=description
        sal = request.form.get('salary') # request.form jest slownikiem pythonowym dlatego uzywamy metody get()
        loc = request.form.get('localisation')
        if len(desc) < 1:
            flash('Description cannot be empty!', category='error')
        elif len(loc) < 1:
            flash('Localisation cannot be empty!', category='error')
        else:
            new_job = Job(user_id=current_user.id, salary=sal, description=desc, localisation=loc)
            db.session.add(new_job)
            db.session.commit()
            flash('Added!', category='success')

    return render_template('home.html', user=current_user) # funkcja zwraca template z pliku home.html

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