from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from .config import Settings
from flask import Flask
import os


app = Flask(__name__)
db = SQLAlchemy()
bcrypt = Bcrypt(app)
jwt = JWTManager()
settings = None
ROOT = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))


def create_app():
  from .config import Config
  cfg = Config(ROOT)
  app.config.from_object(cfg)
  global settings
  settings = Settings(ROOT)
  db.init_app(app)

  from .views import auth, api
  app.register_blueprint(auth, url_prefix='/auth')
  app.register_blueprint(api, url_prefix='/api')

  jwt.init_app(app)

  from .models import User

  @jwt.expired_token_loader
  def expired_token_callback(_jwt_header, jwt_payload):
    return dict(msg='THE'), 401
  
  @jwt.invalid_token_loader
  def invalid_token_callback(reason):
    return dict(msg='TNF'), 401
  
  @jwt.user_lookup_loader
  def user_lookup_callback(_jwt_header, jwt_payload):
    iden = jwt_payload['sub']
    return User.query.filter_by(username=iden).one_or_none()
  
  with app.app_context():
    db.create_all()

  return app
