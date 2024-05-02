import random
from tweetdb import TweetDB

class Randomizer:
    def __init__(self, seed=None):
        self.db = TweetDB()
        if seed:
            random.seed(seed)
        else:
            random.seed()

    def generate_random_number(self, start, end):
        return random.randint(start, end)

    def get_random_tweet(self, only_new, dry_run):
        tweets = []
        if only_new:
            tweets = self.db.get_tweets_by_filter("times=0")
        else:
            tweets = self.db.get_tweets()
        try:
            get_random = self.generate_random_number(0, len(tweets)-1)
        except ValueError:
            raise ValueError("No tweets found")
        if not dry_run:
            self.db.update_tweet(tweets[get_random])
        return tweets[get_random]
