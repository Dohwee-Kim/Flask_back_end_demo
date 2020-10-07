from flask import Flask, request, jsonify

app = Flask(__name__)
app.id_count = 1
app.users = {}
app.tweets = []

@app.route("/ping", methods=['GET'])
def ping():
    return "pong"

@app.route("/sign-up", methods=['POST'])
def sign_up():
    new_user = request.json
    new_user["id"] = app.id_count
    app.users[app.id_count] = new_user
    app.id_count = app.id_count+1

    return jsonify(new_user)

@app.route("/user-counts", methods=['GET'])
def user_counts():
    return jsonify(app.id_count)

@app.route("/tweet", methods=['POST'])
def tweet():
    payload = request.json
    user_id = int(payload['id'])
    tweet = payload['tweet']

    if user_id not in app.users:
        return "User does not exist !", 400

    if len(tweet) > 300:
        return "can not post more than 300 characters", 400

    user_id = int(payload['id'])

    app.tweets.append({'user_id' : user_id,'tweet ' : tweet})
    return "", 200
