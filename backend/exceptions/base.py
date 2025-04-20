from yaml import safe_load
import sys
import os

class Base(BaseException):
  message = None

  def __init__(self, dep, *args) -> None:
    super().__init__(*args)

    self.messages = self._load_messages(dep)
  
  @staticmethod
  def _load_messages(dep):
    fp = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..', 'config', 'messages.yaml'))
    try:
      with open(fp, 'r', encoding='utf-8') as f:
        data = safe_load(f)
      return data[dep]
    except FileNotFoundError:
      print('Exception messages file not found!')
      sys.exit(-1)
  
  def make_error(self, case, error, **kwargs):
    self.message = ' '.join(kwargs.get(word, word) for word in self.messages[case][error].split())
  
  @property
  def json(self):
    return dict(status='error', message=self.message)
