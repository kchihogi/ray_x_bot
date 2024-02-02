import random
from tweetdb import TweetDB

class Randomizer:
    def __init__(self):
        self.db = TweetDB()

    def generate_random_number(self, start, end):
        return random.randint(start, end)

    def get_random_tweet(self):
        tweets = self.db.get_tweets()
        try:
            get_random = self.generate_random_number(0, len(tweets)-1)
        except ValueError:
            return "No tweets found"
        self.db.update_tweet(tweets[get_random])
        return tweets[get_random]
