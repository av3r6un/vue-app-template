from .file_loader import FileLoader
import os


class Settings(FileLoader):
  extra = dict()

  def __init__(self, root) -> None:
    self.ROOT = root
    super().__init__('Settings file')
    self._load_settings()

  def _load_settings(self) -> None:
    data = self.load_settings(os.path.join(self.ROOT, 'config', 'settings.yaml'))
    for name, option in data.items():
      if name.startswith('_'):
        self.extra[name.replace('_', '')] = option
      else:
        self.__dict__[name] = option


