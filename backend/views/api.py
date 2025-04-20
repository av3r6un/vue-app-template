from flask_jwt_extended import jwt_required, current_user
from flask import Blueprint, jsonify, request as req
from backend import settings


api = Blueprint('api', __name__)

@api.route('/', methods=['GET'])
def start():
  import time
  return jsonify(dict(ok=True, current_time=int(time.time())))
