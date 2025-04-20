from .file_loader import FileLoader
from dotenv import load_dotenv
import os


class Config(FileLoader):
  def __init__(self, root) -> None:
    load_dotenv(os.path.join(root, 'config', '.env'))
    self.ROOT = root
    self.SECRET_KEY = os.environ.get('SECRET_KEY')
    self.UNDERDEV = bool(os.getenv('UNDERDEV'))
    self.JWT_SECRET_KEY = self.SECRET_KEY
    super().__init__('Backend settings')
    self._load_settings(os.path.join(self.ROOT, 'config', 'backend.yaml'))
 
  def _load_settings(self, path) -> None:
    data = self.load_settings(path)
    db_uri = f'sqlite:///{os.path.join(self.ROOT, "backend", data.pop("DB_URI", "database.db"))}' if data.get('DB_TYPE', 'local') == 'local' else os.environ.get('DB_URI')
    self.SQLALCHEMY_DATABASE_URI = db_uri
    self.__dict__.update(data)
