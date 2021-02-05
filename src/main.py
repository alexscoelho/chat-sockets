"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask_socketio import SocketIO, send
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

#initialize Flask-SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#Create user
@app.route('/user', methods=['POST'])
def create_user():

    body = request.get_json()
    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'first_name' not in body:
        raise APIException('You need to specify the first_name', status_code=400)
    if 'email' not in body:
        raise APIException('You need to specify the email', status_code=400)
    if 'password' not in body:
        raise APIException('You need to specify the password', status_code=400)

    user1 = User(first_name=body['first_name'], email=body['email'], password=body['password'])
    db.session.add(user1)
    db.session.commit()
    response_body = {
        "msg": "User succesfully created"
    }
    return jsonify(response_body), 200

#Get all users
@app.route('/users', methods=['GET'])
def get_users():

    # get all the people
    users_query = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users_query))
    return jsonify(all_users), 200


# Get or edit a user
@app.route('/user/<int:user_id>', methods=['PUT', 'GET'])
def get_single_user(user_id):
    """
    Single person
    """
    body = request.get_json() 
    if request.method == 'PUT':
        user1 = User.query.get(user_id)
        user1.email = body["email"]
        user1.first_name = body["first_name"]
        db.session.commit()
        return jsonify(user1.serialize()), 200

    if request.method == 'GET':
        user1 = User.query.get(user_id)
        return jsonify(user1.serialize()), 200

    return "Invalid Method", 404

# Delete user
@app.route('/person/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    
    user1 = User.query.get(user_id)
    if user1 is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(user1)
    db.session.commit()
    return jsonify(user1.serialize()), 200

#Event
@socketio.on('message')
def message(message):
    print(message)
    send(message, broadcast=True)
    return None

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    socketio.run(app, debug=True)
    # app.run(host='0.0.0.0', port=PORT, debug=False)
