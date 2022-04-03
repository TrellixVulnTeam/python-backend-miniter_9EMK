from flask import Flask, jsonify, request

app = Flask(__name__)
app.users = {}
app.id_count = 1
app.tweets = []

@app.route("/ping", method=['GET'])
def ping():
    return "pong"

@app.route("/sign-up", method=['POST'])
def sign_up():
    new_user = request.json
    new_user["id"] = app.id_count
    app.users["app.id_count"] = new_user
    app.id_count += 1

    return jsonify(new_user)

@app.route("/tweet", methods=['POST'])
def tweet():
    payload = request.json
    user_id = int(payload['id'])
    tweet = payload['tweet']

    if user_id not in app.users:
        return "No User", 400

    if len(tweet) > 300:
        return 'tweet exceeds 300 characters', 400

    user_id = int(payload['id'])

    app.tweets.append({
        'user_id':user_id,
        'tweet':tweet
    })

    return '', 200

@app.route("/follow", methods=['POST'])
def follow():
    payload = request.json
    user_id = int(payload['id'])
    user_id_to_follow = int(payload['follow'])

    if user_id not in app.users or user_id_to_follow not in app.users:
        return "No User either User or Follower", 400

    user = app.users[user_id]
    user.setdefault('follow',set()).add(user_id_to_follow)
    
    return jsonify(user)

# for postman api connection



