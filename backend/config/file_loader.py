from yaml import safe_load
import sys


class FileLoader:
  def __init__(self, filename = None, **kwargs) -> None:
    self.filename = filename

  def load_settings(self, path) -> dict:
    try:
      with open(path, 'r', encoding='utf-8') as f:
        return safe_load(f)
    except FileNotFoundError:
      print(f'{self.filename} file not found!')
      sys.exit(-1)
