import requests

from seventweets import node_registry


def on_exit(server):
    print("Shutting down Flask application")

    nodes = node_registry.get_all()

    for node in nodes:
        service_url = f'http://{node.address}/registry/{node.name}'
        requests.delete(service_url)