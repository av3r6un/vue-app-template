from backend import db



class ActionLog(db.Model):
  __tablename__ = 'action_logs'

  id: int = db.Column(db.Integer, primary_key=True)
  remote_addr: str = db.Column(db.String(15), nullable=False)
  user_agent: str = db.Column(db.String(255), nullable=True)
  method: str = db.Column(db.String(10), nullable=False)
  content_length: int = db.Column(db.Integer, nullable=False)
  path: str = db.Column(db.String(255), nullable=False)
  status: str = db.Column(db.String(7), nullable=True)

  def __init__(self, remote_addr, method, path, content_length: int = 0, user_agent=None) -> None:
    self.remote_addr = remote_addr
    self.method = method
    self.content_length = content_length if content_length else 0
    self.path = path
    self.user_agent = user_agent

    db.session.add(self)
    db.session.commit()

  @property
  def resolved(self):
    return bool(self.status)

  @property
  def json(self):
    return dict(id=self.id, remote_addr=self.remote_addr, user_agent=self.user_agent, method=self.method, content_length=self.content_length, path=self.path, status=self.st)
  
  @property
  def st(self):
    return self.status
  
  @st.setter
  def st(self, value):
    self.status = value
    db.session.commit()

  def __repr__(self):
    return f'<{self.status.capitalize()} action for {self.path}>'
