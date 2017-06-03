import json

from flask import Flask, request, jsonify
from tweetstorage import TweetDBStorage
from config import Config

storage = None
app = Flask(__name__)

storage = TweetDBStorage()

@app.before_first_request
def init_storage():
    global storage

    if not storage:
        storage = TweetDBStorage()


@app.route('/tweets', methods=['GET'])
def get_tweets():
    tweets = [tweet.to_dict() for tweet in storage.get_all()]
    return jsonify(tweets)


@app.route('/tweets/<int:id_>', methods=['GET'])
def get_tweet(id_):
    tweet = storage.get(id_)
    return jsonify(tweet.to_dict()) if tweet else ("Not found", 404)


@app.route('/tweets', methods=['POST'])
def new_tweet():
    data = request.get_json(force=True)
    tweet_text = json.loads(data)['tweet']
    tweet = storage.add(Config.NODE_NAME, tweet_text)
    return jsonify(tweet.to_dict()), 201


@app.route('/tweets/<int:id_>', methods=['DELETE'])
def delete_tweet(id_):
    storage.remove(id_)
    return '', 204

if __name__ == '__main__':
    app.run(host="0.0.0.0")