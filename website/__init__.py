'''
Taki plik powinien byc tylko jeden.
Dzieki temu folder website bedzie traktowany jako python package.
Po imporcie calego folderu website kod w __init__.py odpali sie automatycznie.
Mozna importowac funkcje z pliku __init__.py w innych plikach.
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# mozna podac do konstrukota aplikacje Flask i nie trzeba potem ustawiac app.app_context() przy tworzeniu tabel
db = SQLAlchemy()

# trzeba przekazac flaskowi widoki stworzone w innych plikach
from .views import views
from .auth import auth

# modele bazy danych importujemy zanim utworzymy baze danych
from .models import User, Ad
from os import path
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'bardzo_trudny_szyfr' # szyfruje dane sesji i pliki cookies
    DB_NAME = 'database.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app) # przekazuje aplikacje z ktorej korzystam do bazy danych

    # rejestrujemy blueprinta i URL pod jakim on jest doczepiony do glownej strony
    app.register_blueprint(blueprint=views, url_prefix='/')
    app.register_blueprint(blueprint=auth, url_prefix='/')

    if not path.exists('website/' + DB_NAME):
        with app.app_context(): # trzeba uzyc with bo w konstruktorze SQLAlchemy() nie podalismy app jako apliakcji Flask
            db.create_all() # tworzy po raz pierwszy tabele bez ich aktualizacji

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # gdzie powinien zostac przekierowany niezalogowany uzytkownik
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) # get domyslnie szuka klucza glownego

    return app

