class TweetStorage:
    tweets = {}
    id_counter = 0

    def get_all(self):
        return [k for k in self.tweets.values()]

    def get(self, id_):
        return self.tweets[id_]

    def add(self, name, tweet_text):
        id_ = self.id_counter
        tweet = {'id': id_, 'name': name, 'tweet': tweet_text}
        self.tweets[id_] = tweet
        self.id_counter = self.id_counter + 1
        return tweet

    def remove(self, id_):
        del self.tweets[id_]
