from flask import Flask, request, jsonify
from flask.json import JSONEncoder

app = Flask(__name__)
app.id_count = 1
app.users = {}
app.tweets = []

class CustomJSONEncoder(JSONEncoder):     #inherited from parent JSONEncoder 
    def default(self, obj):
        if isinstance(obj,set):           #if obj == set
            return list(obj)              #convert it to list 

        return JSONEncoder.default(self, obj)

app.json_encoder = CustomJSONEncoder

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

@app.route("/follow", methods=['POST'])
def follow():
    payload = request.json
    user_id = int(payload['id'])
    want_to_follow_user_id = int(payload['follow'])
    
    #user check 
    if user_id not in app.users:
        return "user {id} does not exist !".format(id=user_id), 400 

    #follower check 
    if want_to_follow_user_id not in app.users:
        return "following user {id} does not exist !".format(id=want_to_follow_user_id), 400

    user = app.users[user_id]
    user.setdefault('follow', set()).add(want_to_follow_user_id) 

    return jsonify(user)

