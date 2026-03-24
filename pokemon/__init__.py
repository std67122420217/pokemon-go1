import os
from flask import Flask
from pokemon.extensions import db, login_manager, bcrypt
from flask_migrate import Migrate
from pokemon.models import User, Type, Pokemon
from pokemon.core.routes import core_bp
from pokemon.users.routes import users_bp
from pokemon.pokemon.routes import pokemon_bp

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'my_super_secret_pokemon_key_12345'
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pokemon.db'
  #app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

  db.init_app(app)
  Migrate(app, db)
  bcrypt.init_app(app)
  login_manager.init_app(app)
  login_manager.login_view = 'users.login'
  login_manager.login_message = 'Please login before access this page!'
  login_manager.login_message_category = 'warning'

  app.register_blueprint(core_bp, url_prefix='/')
  app.register_blueprint(users_bp, url_prefix='/users')
  app.register_blueprint(pokemon_bp, url_prefix='/pokemons')
  
  return app