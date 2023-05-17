'''
Plik zawiera modele bazy danych
'''

# kropka oznacza ten sam folder w ktorym teraz jestesmy
from . import db # importujemy z __init__.py
from flask_login import UserMixin
from sqlalchemy.sql import func

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True) # id samo sie dodaje i nie trzeba go podawac
    salary = db.Column(db.Integer)
    description = db.Column(db.String(1000))
    date = db.Column(db.DateTime, default=func.now()) # ustawia czas na moment dodania ogloszenia
    localisation = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # klasa User w SQL bedzie zapisana jako obiekt user

# dla usera dodatkowe dziedziczenie po UserMixin zeby mozna bylo uzywac obiektu current_user() z flask_login
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True) # unique zapewnia ze bedzie tylko jeden taki mail
    password = db.Column(db.String(30))
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    jobs = db.relationship('Job') # tutaj juz nazwa klasy pythonowej