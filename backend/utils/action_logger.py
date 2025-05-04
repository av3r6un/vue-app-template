from sqlalchemy.exc import IntegrityError
from contextvars import ContextVar
from functools import wraps


class Actions:
  def __init__(self, name: str):
    self.cid = ContextVar('current_id')
    self.name = self._validate_name(name)

  def __call__(self, handler):
    @wraps(handler)
    def wrapper(*args, **kwargs):
      from flask import request as req, jsonify
      from backend.models import ActionLog
      try:
        action = ActionLog(req.remote_addr, req.method, req.full_path, content_length=req.content_length, user_agent=req.headers.get('User-Agent'))
        token = self.cid.set(action.id)
        try:
          return handler(*args, **kwargs)
        finally:
          self.cid.reset(token)
      except IntegrityError:
        return jsonify(dict(status='error', message='Bad request')), 400
    return wrapper
  
  @staticmethod
  def _validate_name(name: str):
    if len(name.split('.')) > 1:
      return name.split('.')[-1]
    return name

  def result(self, status='success'):
    from backend.models import ActionLog
    currentId = self.cid.get(None)
    if not currentId:
      raise RuntimeError('No currentId!')
    action = ActionLog.query.filter_by(id=currentId).one_or_none()
    if not action:
      raise RuntimeError('Bad actionID!')
    action.st = status
    return action.json
    