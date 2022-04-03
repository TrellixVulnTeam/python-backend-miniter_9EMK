from flask import Flask, jsonify, request

app = Flask(__name__)
app.tweets = []

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
    
