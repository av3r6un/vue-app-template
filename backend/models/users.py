from flask_jwt_extended import create_access_token, create_refresh_token
from backend.exceptions import ValidationError
from backend import db, settings, bcrypt
from backend.utils import create_uid
from datetime import datetime as dt
from user_agents import parse
import string
import os
import re


class User(db.Model):
  __tablename__ = 'users'

  uid = db.Column(db.String(6), primary_key=True)
  username = db.Column(db.String(50), nullable=False, unique=True)
  email = db.Column(db.String(100), nullable=False, unique=True)
  password = db.Column(db.String(255), nullable=False)
  avatar = db.Column(db.String(255), nullable=True)
  reg_date = db.Column(db.Integer, nullable=False, default=int(dt.now().timestamp()))
  last_date = db.Column(db.Integer, nullable=False)
  reg_ip = db.Column(db.String(15), nullable=False)
  last_ip = db.Column(db.String(15), nullable=False)
  last_device = db.Column(db.String(16), db.ForeignKey('devices.uid'), nullable=False)

  def __init__(self, username: str, email: str, passwords: tuple[str, str], reg_ip: str, user_agent: str, reg_date: int = None) -> None:
    self.uid = create_uid(6, [a.uid for a in self.query.all()])
    self.username = self._validate_username(username)
    self.email = self._validate_email(email)
    self.password = self._validate_passwords(passwords)
    self.reg_ip = reg_ip
    self.reg_date = reg_date if reg_date else int(dt.now().timestamp())
    self.last_ip = reg_ip
    self.last_date = self.reg_date
    device = Device(self.uid, user_agent)
    self.last_device = device.uid

    db.session.add(self)
    db.session.commit()

  @staticmethod
  def _validate_passwords(passwords: tuple) -> None:
    p1, p2 = passwords   
    pattern = rf'{settings.STRONG_PASSWORD_PATTERN}'
    if not p1 or not p2:
      raise ValidationError('register', 'password_absence')
    if p1 != p2:
      raise ValidationError('register', 'passwords_mismatch')
    if not re.match(pattern, p1) and p1 != os.getenv('ADMIN_PASSWORD'):
      raise ValidationError('register', 'week_password')
    return bcrypt.generate_password_hash(p1)

  @classmethod
  def login(cls, username, password, last_ip, user_agent, **kwargs) -> dict:
    user = cls.query.filter_by(username=username).first()
    if not user:
      raise ValidationError('login', 'not_found')
    return user._login(password, last_ip, user_agent)

  @classmethod
  def refresh(cls, iden) -> str:
    return create_access_token(identity=iden, fresh=False)
  
  def _validate_username(self, username) -> str:
    user = self.query.filter_by(username=username).first()
    alp = string.ascii_letters + string.digits + string.punctuation
    if user:
      raise ValidationError('register', 'username_exists')
    if len(username) < 5 and username != os.getenv('ADMIN_USERNAME'):
      raise ValidationError('register', 'short_username')
    forbidden_letter = [l for l in username if l not in alp]
    if len(forbidden_letter) >= 1: raise ValidationError('register', 'lang')
    return username
  
  def _validate_email(self, email) -> str:
    em_exists = self.query.filter_by(email=email).first()
    pattern = rf'{settings.EMAIL_PATTERN}'
    if em_exists:
      raise ValidationError('register', 'email_exists')
    if not re.match(pattern, email):
      raise ValidationError('register', 'email_validity')
    return email
  
  
  def _login(self, password, last_ip, user_agent) -> dict:
    if not bcrypt.check_password_hash(self.password, password):
      raise ValidationError('register', 'passwords_mismatch')
    self.last_ip = last_ip
    device = Device(self.uid, user_agent)
    self.last_device = device.uid
    extra = dict(
      accs_token=create_access_token(self.username, fresh=True),
      rfsh_token=create_refresh_token(self.username)
    )
    db.session.commit()
    return self.collect_info(**dict(tokens=extra))
  
  def collect_info(self, **kwargs) -> dict:
    info = self.base_info
    info.update(kwargs)
    return info
  
  @property
  def base_info(self) -> dict:
    return dict(uid=self.uid, username=self.username, email=self.email)
  
  @property
  def json(self):
    bi = self.base_info
    bi.update(dict(last_ip=self.last_ip, last_date=self.last_date, last_device=self.last_device))
    return bi
  

class Device(db.Model):
  __tablename__ = 'devices'

  uid = db.Column(db.String(16), primary_key=True)
  used_by = db.Column(db.String(6), db.ForeignKey(User.uid), nullable=False)
  browser = db.Column(db.String(30), nullable=False)
  browser_version = db.Column(db.Text, nullable=False)
  os = db.Column(db.String(20), nullable=False)
  os_version = db.Column(db.Text, nullable=False)
  device = db.Column(db.String(30), nullable=False)
  user_agent = db.Column(db.Text, nullable=False)

  def __init__(self, user_uid: str, user_agent: str, **kwargs) -> None:
    self.uid = create_uid(16, [a.uid for a in self.query.all()])
    self.used_by = user_uid
    self._parse_user_agent(user_agent)
    if self._is_new_device():
      db.session.add(self)
      db.session.commit()

  def _is_new_device(self):
    found = self.query.filter_by(user_agent=self.user_agent).first()
    if not found: return True
    self.uid = found.uid
    return False

  def _parse_user_agent(self, user_agent):
    self.user_agent = user_agent
    ua = parse(user_agent)
    self.browser = ua.browser.family
    self.browser_version = ua.browser.version_string
    self.os = ua.os.family
    self.os_version = ua.os.version_string
    self.device = ua.device.family
    
  @property
  def ua(self):
    return dict(browser=self.browser, browser_version=self.browser_version, os=self.os, os_version=self.os_version, device=self.device)
  
  @property
  def json(self):
    info = self.ua
    info.update(dict(used_by=self.used_by))
    return info
  


  