# from flask import Blueprint, jsonify, request
# from flask_jwt_extended import create_access_token

# login_blueprint = Blueprint('logic', __name__)


# @login_blueprint.route('/login', methods=['POST'])
# def login():
#   username = request.json.get('username', None)
#   password = request.json.get('password', None)

#   if username != 'admin' or password != 'password':
#     return jsonify({"msg": "Bad username or password"}), 401
  
#   access_token = create_access_token(identify=username)
#   return jsonify(access_token=access_token)