import json
import requests

from flask import Flask, request, jsonify
from tweetstorage import TweetDBStorage
from noderegistry import NodeRegistry
from config import Config
from auth import auth

storage = None
node_registry = None
app = Flask(__name__)


@app.before_first_request
def init_storage():
    global storage
    global node_registry

    if not storage:
        storage = TweetDBStorage()

    if not node_registry:
        node_registry = NodeRegistry()


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
@auth
def delete_tweet(id_):
    storage.remove(id_)
    return '', 204


@app.route('/registry', methods=['POST'])
def register_node():
    data = json.loads(request.get_json(force=True))
    node_name = data['name']
    node_address = data['address']
    nodes = node_registry.add(node_name, node_address)
    nodes = [node.to_dict() for node in nodes]
    return jsonify(nodes), 201


@app.route('/registry/<name>', methods=['DELETE'])
def remove_node(name):
    node_registry.remove(name)
    return '', 204


@app.route('/join_network', methods=['POST'])
def join_network():

    if len(node_registry.get_all()):
        data = json.loads(request.get_json(force=True))
        node_name = data['name']
        node_address = data['address']

        node_registry.add(node_name, node_address)

        service_url = f'http://{node_address}/registry'
        response = requests.post(service_url,
                             json={"name": node_name, "address": node_address})

        nodes = json.loads(response.get_json(force=True))

        for node in nodes:
            node_name = node['name']
            if node_registry.conains(node_name):
                continue

            node_address = node['address']
            service_url = f'http://{node_address}/registry'
            requests.post(service_url,
                          json={"name": Config.NODE_NAME, "address": Config.NODE_ADDRESS})
            node_registry.add(node_name, node_address)

if __name__ == '__main__':
    app.run(host="127.0.0.1")
