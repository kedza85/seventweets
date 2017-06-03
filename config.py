import os
import binascii


def generate_api_token():
    """
    Generates random token.
    """
    return binascii.b2a_hex(os.urandom(15))


class Config(object):
    DB_CONFIG = dict(host=os.environ.get('SEVENTWEETS_DB_HOST', 'localhost'),
                     port=int(os.environ.get('SEVENTWEETS_DB_PORT', 5432)),
                     database=os.environ.get('SEVENTWEETS_DB_NAME', 'radionica'),
                     user=os.environ.get('SEVENTWEETS_DB_USER', 'radionica'),
                     password=os.environ.get('SEVENTWEETS_DB_PASS', None),
                     unix_sock=None, ssl=None, timeout=None)

    NODE_NAME = os.environ.get('SEVENTWEETS_NODE_NAME', 'kedza')
    API_TOKEN = os.environ.get('SEVENTWEETS_API_TOKEN', generate_api_token())
