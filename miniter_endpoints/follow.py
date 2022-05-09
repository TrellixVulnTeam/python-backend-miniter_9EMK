from flask import Flask, jsonify, request

app = Flask(__name__)

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
    