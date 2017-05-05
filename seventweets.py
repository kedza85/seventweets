import json

from flask import Flask, request, jsonify
from tweetstorage import TweetStorage

app = Flask(__name__)
storage = TweetStorage()
name = 'Kedza'


@app.route('/tweets', methods=['GET'])
def get_tweets():
    tweets = [tweet for tweet in storage.get_all()]
    return jsonify(tweets)


@app.route('/tweets/<int:id_>', methods=['GET'])
def get_tweet(id_):
    tweet = storage.get(id_)
    return jsonify(tweet)


@app.route('/tweets', methods=['POST'])
def new_tweet():
    data = request.get_json(force=True)
    tweet_text = json.loads(data)['tweet']
    tweet = storage.add(name, tweet_text)
    return jsonify(tweet), 201


@app.route('/tweets/<int:id_>', methods=['DELETE'])
def delete_tweet(id_):
    storage.remove(id_)
    return '', 204

if __name__ == '__main__':
    app.run(host="0.0.0.0")