from .base import Base

class ValidationError(Base):
  def __init__(self, case, error, *args, **kwargs) -> None:
    super().__init__('validation', *args)
    self.make_error(case, error, **kwargs)
