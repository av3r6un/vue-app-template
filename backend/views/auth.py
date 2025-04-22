from flask_jwt_extended import jwt_required, current_user, get_jwt_identity
from flask import Blueprint, jsonify, request as req
from backend.exceptions import ValidationError
from backend.models import User


auth = Blueprint('auth', __name__)


@auth.route('/', methods=['POST'])
def login():
  user_data = req.get_json()
  user_data['last_ip'] = req.remote_addr
  user_data['user_agent'] = req.headers.get('User-Agent')
  try:
    creds = User.login(**user_data)
    return jsonify(dict(status='success', body=creds))
  except ValidationError as valid:
    return jsonify(valid.json), 400
  
@auth.route('/me', methods=['GET'])
@jwt_required()
def user_info():
  return jsonify(dict(status='success', body=current_user.json))

@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
  iden = get_jwt_identity()
  token = User.refresh(iden)
  return jsonify(dict(status='success', token=token))

@auth.route('/register', methods=['POST'])
def register():
  data = req.get_json()
  data['reg_ip'] = req.remote_addr
  data['user_agent'] = req.headers.get('User-Agent')
  try:
    creds = User(**data)
    return jsonify(dict(status='success', body=None))
  except ValidationError as valid:
    return jsonify(valid.json), 400
