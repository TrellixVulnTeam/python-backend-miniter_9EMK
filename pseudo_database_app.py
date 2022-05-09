from flask import Flask, jsonify, request
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text # hope this works

# JSON data doesn't allow "set" type data
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return JSONEncoder.default(self, obj)


# Create Databases
def get_user(user_id):
    user = app.database.execute(text("""
        SELECT
            id,
            name,
            email,
            profile
        FROM users
        WHERE id = :user_id
        """), {
        'user_id' : user_id
        }).fetchone()

    return {
        'id' : user['id'],
        'name' : user['name'],
        'email' : user['email'],
        'profile' : user['profile']
    } if user else None


def insert_user(user):
    return app.database.execute(text("""
        INSERT INTO users (
            name,
            email,
            profile,
            hashed_password
        ) VALUES (
            :name,
            :email,
            :profile,
            :password
        )
        """), user).lastrowid

def insert_tweet(user_tweet):
    return app.database.execute(text("""
        INSERT INTO tweets (
            user_id,
            tweet
        ) VALUES (
            :id,
            :tweet,
        )
        """), user_tweet).rowcount


def insert_follow(user_follow):
    return app.database.execute(text("""
        INSERT INTO users_follow_list (
            user_id,
            follow_user_id
        ) VALUES (
            :id,
            :follow,
        )
        """), user_follow).rowcount


def insert_unfollow(user_unfollow):
    return app.database.execute(text("""
        DELETE FROM users_follow_list
        WHERE user_id = :id
        AND follow_user_id = :unfollow
        """), user_unfollow).rowcount

# resume from here
def get_timeline(user_id):
    return app.database.execute(text("""
        INSERT INTO users_follow_list (
            user_id,
            follow_user_id
        ) VALUES (
            :id,
            :follow,
        )
        """), user_follow).rowcount



    
    
# Create API & Endpoints
app = Flask(__name__)

app.json_encoder = CustomJSONEncoder

app.users = {}
app.id_count = 1
app.tweets = []


@app.route('/')
def hello_world():
    return "Hello, Python!"


@app.route("/ping")
def ping():
    return "pong"


@app.route("/sign_up", methods=["POST"])
def sign_up():
    new_user = request.json
    new_user["id"] = app.id_count
    app.users[app.id_count] = new_user
    app.id_count += 1

    return jsonify(new_user)


@app.route("/get_users", methods=["GET"])
def get_users():
    return app.users
# {"app.id_count":{"email": "kevin4623@gmail.com",
#     "id":1, "name":"Kevin", "password": "test1234"}}


@app.route("/tweet", methods=["POST"])
def tweet():
    payload = request.json
    user_id = int(payload['id'])
    tweet = payload['tweet']

    if user_id not in app.users:
        return "No User", 400

    if len(tweet) > 300:
        return 'tweet exceeds 300 characters', 400

    user_id = int(payload['id'])

    app.tweets.append({'user_id': user_id, 'tweet': tweet})

    return '', 200


@app.route("/follow", methods=['POST'])
def follow():
    payload = request.json
    user_id = int(payload['id'])
    user_id_to_follow = int(payload['follow'])

    if user_id not in app.users or user_id_to_follow not in app.users:
        return "No User ID. Please verify user or follow id", 400

    user = app.users[user_id]
    user.setdefault('follow', set()).add(user_id_to_follow)

    return jsonify(user)


@app.route("/unfollow", methods=['POST'])
def unfollow():
    payload = request.json
    user_id = int(payload['id'])
    user_id_to_unfollow = int(payload['unfollow'])

    if user_id not in app.users or user_id_to_unfollow not in app.users:
        return 'No User ID. Please verify user and unfollow id', 400

    user = app.users['user_id']
    user.setdefault('follow', set()).discard(user_id_to_unfollow)

    return jsonify(user)


@app.route("/timeline/<int:user_id>", methods=['GET'])
def timeline(user_id):
    if user_id not in app.users:
        return 'No User ID', 400

    follow_list = app.users[user_id].get('follow', set())
    follow_list.add(user_id)
    timeline = [
        tweet for tweet in app.tweets if tweet['user_id'] in follow_list
    ]

    return jsonify({'user_id': user_id, 'timeline': timeline})


app.run(host='0.0.0.0', port=5000, debug=True)
