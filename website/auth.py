from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash # szyfrowanie hasel
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint(name='auth', import_name=__name__)

# methods - arugment z requestami ktore route moze przyjac, domyslnie GET
@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form # slownik informacji o requescie np. url, metoda, informacje z form jak email itp.
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first() # pierwszy user z podanym mailem
        if user:
            # sprawdzamy, czy hash podanego hasla sie zgadza z haslem w bazie danych
            if check_password_hash(user.password, password):
                flash('Zalogowano!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.account'))
            else:
                flash('Niepoprawne hasło!', category='error')
        else:
            flash('Podany adres e-mail nie istnieje!', category='error')

    return render_template('login.html', user=current_user) # mozna przekazywac zmienne do widokow

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user: # jezeli uzytkownik istnieje to wyswietla wiadomosc
            flash('Podany e-mail znajduje się już w bazie danych!', category='error')
        elif len(email) < 4:
            flash(message='E-mail jest za krótki!', category='error')
        elif len(firstName) < 2:
            flash(message='Pole imię nie może być puste!', category='error')
        elif len(lastName) < 2:
            flash(message='Pole nazwisko nie może być puste!', category='error')
        elif len(password1) < 8:
            flash(message='Podane hasło jest zbyt krótkie', category='error')
        elif password1 != password2:
            flash(message='Hasła nie zgadzają się!', category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(password1, method='sha256'), first_name=firstName, last_name=lastName)
            db.session.add(new_user)
            db.session.commit() # update bazy danych
            login_user(new_user, remember=True) # logowanie uzytkownika po rejestracji
            flash(message='Konto utworzone!', category='success')

            # przekierowujemy na url uzywajac funkcji pythonowej ktora renderuje template
            return redirect(url_for('views.account'))
    return render_template('sign_up.html', user=current_user)