import os
import tweepy

def main():
    BEARER_TOKEN = os.environ['BEARER_TOKEN']
    API_KEY = os.environ['API_KEY']
    API_KEY_SECRET = os.environ['API_KEY_SECRET']
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_KEY_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )
    client.create_tweet(text="Hello, world!")

if __name__ == "__main__":
    main()
