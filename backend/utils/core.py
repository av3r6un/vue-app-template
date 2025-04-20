from backend.exceptions import ValidationError
import secrets
import string

def create_uid(length, uids):
  alp = string.ascii_letters + string.digits
  while True:
    uid = ''.join(secrets.choice(alp) for _ in range(length))
    if uid not in uids:
      return uid
    