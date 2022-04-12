@app.route("/timeline/<int user_id>", methods=['GET'])
def timeline(user_id):
    if user_id not in app.users:
        return 'No User ID', 400

    follow_list = app.users[user_id].get('follow', set())
    follow_list.add(user_id)
    timeline = [tweet for tweet in app.tweets if tweet['user_id'] in follow_list]

    return jsonify(
        {
            'user_id':user_id,
            'timeline': timeline
        }
    )

