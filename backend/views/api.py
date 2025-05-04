from flask_jwt_extended import jwt_required, current_user
from flask import Blueprint, jsonify, request as req
from backend.utils import Actions
from backend.utils import setup_logger
from backend import settings


api = Blueprint('api', __name__)
actions = Actions(__name__)
logger = setup_logger('API-HANDLER')


@api.route('/', methods=['GET'])
@actions
def start():
  import time
  actions.result()
  return jsonify(dict(ok=True, current_time=int(time.time())))

