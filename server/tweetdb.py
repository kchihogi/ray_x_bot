import os
import datetime
from db import DB
from models import TweetModel

class TweetDB:
    tables = [
        TweetModel,
    ]

    def __init__(self):
        self.db = DB(os.environ['DB_FILE'] if 'DB_FILE' in os.environ else "ray_x_bot.db")
        self.db.connect()
        for table in self.tables:
            instance = table()
            self.db.create_table(instance.table_name, instance.columns(with_type=True))

    def add_tweet(self, tweet_model):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tweet_model.setter(created_at=now, last_updated=now, times=0)
        tuple_values = tweet_model.to_tuple()
        columns = tweet_model.columns()
        t_str = ""
        c_str = ""
        # delete none values
        for i in range(len(tuple_values)):
            if tuple_values[i] is not None:
                t_str += f"{tuple_values[i]},"
                c_str += f"{columns.split(',')[i]},"
        self.db.insert(tweet_model.table_name, c_str[:-1], t_str[:-1])

    def delete_tweet(self, id):
        self.db.delete("tweets", f"id = {id}")

    def update_tweet(self, tweet_model):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        times = tweet_model.times["value"] + 1 if tweet_model.times["value"] is not None else 1
        tweet_model.setter(last_updated=now, times=times)
        set_str = ""
        for attr in tweet_model.to_dict():
            if tweet_model.to_dict()[attr] is not None:
                set_str += f"{attr} = {tweet_model.to_dict()[attr]},"
        self.db.update(tweet_model.table_name, set_str[:-1], f"id = {tweet_model.to_dict()['id']}")

    def get_tweet(self, id):
        tweet = self.db.select(self.tables[0]().table_name, self.tables[0]().columns(), f"id = {id}")
        return TweetModel(*tweet[0])

    def get_tweets(self):
        tweets = self.db.select(self.tables[0]().table_name, self.tables[0]().columns())
        tweet_list = []
        for tweet in tweets:
            tweet_list.append(TweetModel(*tweet))
        return tweet_list
    
    def get_tweets_by_filter(self, filter):
        tweets = self.db.select(self.tables[0]().table_name, self.tables[0]().columns(), filter)
        tweet_list = []
        for tweet in tweets:
            tweet_list.append(TweetModel(*tweet))
        return tweet_list
    
    def get_tweets_by_limit(self, limit):
        tweets = self.db.select(self.tables[0]().table_name, self.tables[0]().columns(), limit=limit)
        tweet_list = []
        for tweet in tweets:
            tweet_list.append(TweetModel(*tweet))
        return tweet_list
    
    def get_tweets_by_filter_and_limit(self, filter, limit):
        tweets = self.db.select(self.tables[0]().table_name, self.tables[0]().columns(), filter, limit)
        tweet_list = []
        for tweet in tweets:
            tweet_list.append(TweetModel(*tweet))
        return tweet_list

    def __del__(self):
        self.db.disconnect()

    def drop_all_tables(self):
        for table in self.tables:
            self.db.drop_table(table().table_name)

    def create_all_tables(self):
        for table in self.tables:
            instance = table()
            self.db.create_table(instance.table_name, instance.columns(with_type=True))

if __name__ == "__main__":
    db = TweetDB()

    db.drop_all_tables()
    db.create_all_tables()

    model = TweetModel(text="Hello, world!", image=None)
    db.add_tweet(model)
    tweets = db.get_tweets()
    print(len(tweets))
    if len(tweets) > 0:
        id = tweets[0].id["value"]
        tweet = tweets[0]
        tweet.setter(text="Updated tweet!", image=None)
        db.update_tweet(tweet)
        print(db.get_tweet(id))
        tweet.setter(text="Updated tweet again!", image=None)
        db.update_tweet(tweet)
        print(db.get_tweet(id))
        db.delete_tweet(id)
        print(len(db.get_tweets()))

    for i in range(40):
        model = TweetModel(text=f"Hello, world! {i}", image=None)
        db.add_tweet(model)

    print("----------------------")
    tweets = db.get_tweets()
    print(len(tweets))
    for tweet in tweets:
        print(tweet)
    print(len(db.get_tweets_by_limit(5)))
    print(len(db.get_tweets_by_filter("text like '%5%'")))
    print(len(db.get_tweets_by_filter_and_limit("text like '%5%'", 2)))

