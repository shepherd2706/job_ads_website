'''
Zawiera URL do komponentow strony
'''

from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Ad
from . import db
import json

views = Blueprint(name='views', import_name=__name__)

# to co w home odpali sie gdy wejde w URL tego konkretnego widoku
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        ad = request.form.get('ad') # dane z forma o id=ad
        if len(ad) < 1:
            flash('Text is too short!', category='error')
        else:
            new_ad = Ad(user_id=current_user.id, salary=1000, description=ad, place='Warsaw')
            db.session.add(new_ad)
            db.session.commit()
            flash('Added!', category='success')

    return render_template('home.html', user=current_user) # funkcja zwraca template z pliku home.html

'''
@views.route('/delete-ad', methods=['POST'])
def delete_ad():
    ad = json.loads(request.data)
'''