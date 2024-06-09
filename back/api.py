from flask import Flask, request, jsonify
from functools import wraps
from os import environ
import redis
import jwt
from hashlib import sha256
import datetime
import time
import json

app = Flask(__name__)
app.config['REDIS_HOST'] = environ['DB_HOST']
app.config['REDIS_PORT'] = environ['DB_PORT']
app.config['REDIS_PASSWORD'] = environ['DB_PASSWORD']

redis_client = redis.Redis(
    host=app.config['REDIS_HOST'],
    port=app.config['REDIS_PORT'],
    password=app.config['REDIS_PASSWORD'],
    decode_responses=True)
DEFAULT_EXPIRATION_MINUTES = 15


# função básica de autenticação, decodifica com checks de username alegado e expiração
def decode_jwt_token(token, username):
    return jwt.decode(token,
                      environ['JWT_SECRET'],
                      audience=f'urn:{username}',
                      algorithms=['HS256'],
                      options={'require': ['exp', 'aud']})


# decorator que verifica em requests que exigem jwt token do usuário
def jwt_token_required(a_route):
    @wraps(a_route)
    def decorator(*args, **kwargs):
        token = None
        username = None
        if 'x-access-token' in request.headers and 'username' in request.headers:
            token = request.headers['x-access-token']
            username = request.headers['username']
        if (not token) or (not username):
            return "Missing either token or username", 401
        try:
            decode_jwt_token(token, username)
        except (jwt.InvalidAudienceError, jwt.ExpiredSignatureError) as _:
            return 'Invalid token', 401
        return a_route(*args, **kwargs)
    return decorator


def create_user_token(username):
    return jwt.encode({
        'aud': f'urn:{username}',
        'exp': int(time.time()) + DEFAULT_EXPIRATION_MINUTES * 60,
    },  environ['JWT_SECRET'])


STATIC_SALT = environ['SALT']


def calc_rehashed_password(hashed_password, dynamic_salt_username):
    return sha256(
        f'{hashed_password}:{dynamic_salt_username}:{STATIC_SALT}'.encode()
    ).hexdigest()


def create_default_coordinates(username):
    with open('positions.json', 'r') as f:
        positions = json.load(f)
        positions = get_valid_user_coordinates(positions['data'])
    redis_client.set(
        f'user-coordinates/{username}', json.dumps(positions))


@app.route(f'/users', methods=["POST"])
def post_user_registration():
    registration_data = request.json
    username = registration_data.get('username')
    user = {
        'username': username,
        'rehashed_password': calc_rehashed_password(
            registration_data.get('hashed_password'),
            username)
    }

    user_path = f'users/{username}'

    existent_user = redis_client.get(user_path)

    if not (existent_user is None):
        return '', 500

    redis_client.set(user_path, json.dumps(user))

    try:
        create_default_coordinates(username)
    except (FileNotFoundError,
            PermissionError,
            IsADirectoryError,
            IOError) as _:
        redis_client.delete(user_path)
        return 'Internal Server Error', 501

    return create_user_token(username), 201


@app.route(f'/login', methods=["GET"])
def get_user_login():
    username = request.args.get('username')
    user_path = f'users/{username}'

    redis_user = redis_client.get(user_path)

    if redis_user is None:
        return '', 401

    redis_user = json.loads(redis_user)

    if calc_rehashed_password(
            request.args.get('hashed_password'),
            username) != redis_user['rehashed_password']:
        return '', 401

    return create_user_token(username), 202


@app.route(f'/user-coordinates/<username>', methods=["GET"])
@jwt_token_required
def get_user_coordinate(username: str):
    if username != request.headers['username']:
        return '', 401
    username = str(username)
    redis_user_coordinates = redis_client.get(
        f'user-coordinates/{username}')

    if redis_user_coordinates is None:
        return '', 404

    redis_user_coordinates = json.loads(redis_user_coordinates)

    return jsonify(redis_user_coordinates), 200


def get_valid_user_coordinate(user_coordinate):
    a_valid_user_coordinate = {}
    a_valid_user_coordinate['date_time'] = datetime.datetime.fromisoformat(
        user_coordinate['date_time']).isoformat()
    a_valid_user_coordinate['latitude'] = float(user_coordinate['latitude'])
    a_valid_user_coordinate['longitude'] = float(user_coordinate['longitude'])
    return a_valid_user_coordinate


def get_valid_user_coordinates(user_coordinates_body: list) -> list:
    valid_user_coordinates = []
    for user_coordinate in user_coordinates_body:
        valid_user_coordinates.append(
            get_valid_user_coordinate(user_coordinate))
    return valid_user_coordinates


@app.route(f'/user-coordinates/<username>', methods=["POST"])
@jwt_token_required
def post_user_coordinates(username: str):
    if username != request.headers['username']:
        return '', 401
    user_coordinates = get_valid_user_coordinates(request.json)

    redis_client.set(
        f'user-coordinates/{username}', json.dumps(user_coordinates))

    return '', 201


@app.route(f'/user-coordinates/<username>', methods=["PUT"])
@jwt_token_required
def put_user_coordinate(username: str):
    if username != request.headers['username']:
        return '', 401
    user_coordinate = get_valid_user_coordinate(request.json)

    user_coordinates = redis_client.get(
        f'user-coordinates/{username}')

    user_coordinates = [] if user_coordinates is None else json.loads(
        user_coordinates)

    user_coordinates.append(user_coordinate)

    redis_client.set(
        f'user-coordinates/{username}', json.dumps(user_coordinates))

    return '', 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
