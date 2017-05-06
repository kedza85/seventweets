from tweetstorage import TweetStorage


def test_get_all():
    storage = TweetStorage()
    tweets = storage.get_all()
    assert isinstance(tweets, list)
    assert len(tweets) == 0

    storage.tweets = {0: {'id': 0, 'name': 'test name', 'tweet': 'test tweet'}}
    tweets = storage.get_all()
    assert isinstance(tweets, list)
    assert len(tweets) == 1
    tweet = tweets[0]
    assert tweet['id'] == 0
    assert tweet['name'] == 'test name'
    assert tweet['tweet'] == 'test tweet'


def test_get():
    storage = TweetStorage()

    tweet = storage.get(0)
    assert tweet is None

    storage.tweets = {0: {'id': 0, 'name': 'test name', 'tweet': 'test tweet'}}

    tweet = storage.get(0)
    assert tweet is not None
    assert tweet['id'] == 0


def test_add():
    storage = TweetStorage()

    tweet = storage.add('test name', 'test tweet')
    assert tweet['id'] == 0
    assert tweet['name'] == 'test name'
    assert tweet['tweet'] == 'test tweet'

    tweets = storage.get_all()
    assert len(tweets) is 1


def test_remove():
    storage = TweetStorage()
    storage.tweets = {0: {'id': 0, 'name': 'test name', 'tweet': 'test tweet'}}

    storage.remove(0)
    tweets = storage.get_all()
    assert len(tweets) == 0
