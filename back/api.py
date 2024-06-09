from flask import Flask, request, jsonify
from os import environ
import redis
import jwt
from hashlib import sha256
import time

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


def create_user_token(username):
    return jwt.encode({
        'aud': f'urn:{username}',
        'exp': int(time.time()) + DEFAULT_EXPIRATION_MINUTES * 60,
    },  environ['JWT_SECRET'],
        algorithms=['HS256'])


STATIC_SALT = environ['SALT']


def calc_rehashed_password(hashed_password, dynamic_salt_username):
    return sha256(
        f'{hashed_password}:{dynamic_salt_username}:{STATIC_SALT}'.encode()
    ).hexdigest()


@app.route("/users", methods=["POST"])
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
        return 'could not handle request', 500

    redis_client.set(user_path, jsonify(user).get_data(as_text=True))

    return create_user_token(username), 201


def is_auth_user(token, username):
    return jwt.decode(token,
                      environ['JWT_SECRET'],
                      audience=f'urn:{username}',
                      algorithms=['HS256'],
                      options={'require': ['exp', 'aud']})


@ app.route("/user-coordinates", methods=["GET"])
def getUserCoordinates():
    user_id = request.args.get('userId')
    try:
        is_auth_user(request.headers.get('jwt'),
                     request.headers.get('username'))

        redis_user_coordinates = redis_client.get(
            f'user-coordinates/{user_id}')

        if redis_user_coordinates is None:
            return '', 404
        return jsonify(redis_user_coordinates), 200
    except (jwt.InvalidAudienceError, jwt.ExpiredSignatureError) as _:
        return '', 401

    return
    return [{
        "date_time": "2019-02-12T10:57:36+00:00",
        "latitude": "-18.92406700",
        "longitude": "-48.28214200"
    },
        {
        "date_time": "2019-02-12T10:57:06+00:00",
        "latitude": "-18.92376500",
        "longitude": "-48.28210800"
    },
        {
        "date_time": "2019-02-12T10:56:36+00:00",
        "latitude": "-18.92213500",
        "longitude": "-48.28205200"
    },
        {
        "date_time": "2019-02-12T10:56:06+00:00",
        "latitude": "-18.92082200",
        "longitude": "-48.28132800"
    },
        {
        "date_time": "2019-02-12T10:55:36+00:00",
        "latitude": "-18.91951300",
        "longitude": "-48.28033200"
    },
        {
        "date_time": "2019-02-12T10:55:06+00:00",
        "latitude": "-18.91966300",
        "longitude": "-48.27849800"
    },
        {
        "date_time": "2019-02-12T10:54:36+00:00",
        "latitude": "-18.92081800",
        "longitude": "-48.27682200"
    },
        {
        "date_time": "2019-02-12T10:54:06+00:00",
        "latitude": "-18.92195000",
        "longitude": "-48.27513200"
    },
        {
        "date_time": "2019-02-12T10:53:36+00:00",
        "latitude": "-18.92298100",
        "longitude": "-48.27350800"
    },
        {
        "date_time": "2019-02-12T10:53:06+00:00",
        "latitude": "-18.92313700",
        "longitude": "-48.27337200"
    },
        {
        "date_time": "2019-02-12T10:52:36+00:00",
        "latitude": "-18.92372200",
        "longitude": "-48.27213800"
    },
        {
        "date_time": "2019-02-12T10:52:06+00:00",
        "latitude": "-18.92295000",
        "longitude": "-48.27078200"
    },
        {
        "date_time": "2019-02-12T10:51:36+00:00",
        "latitude": "-18.91990800",
        "longitude": "-48.26785500"
    },
        {
        "date_time": "2019-02-12T10:51:06+00:00",
        "latitude": "-18.91765300",
        "longitude": "-48.26528000"
    },
        {
        "date_time": "2019-02-12T10:50:36+00:00",
        "latitude": "-18.91815100",
        "longitude": "-48.26453900"
    },
        {
        "date_time": "2019-02-12T10:50:06+00:00",
        "latitude": "-18.91814500",
        "longitude": "-48.26453700"
    }], 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
