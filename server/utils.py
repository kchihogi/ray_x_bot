import argparse
from tweetdb import TweetDB
from models import TweetModel

def list_tweets(db, limit, filter, csv):
    try:
        if filter:
            filter = f"text like '%{filter}%'"
        if limit < 0:
            limit = None
        tweets = db.get_tweets_by_filter_and_limit(filter, limit)
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    if csv:
        print("id,text,created_at,last_updated,times,image")
        for tweet in tweets:
            print("{},{},{},{},{},{}".format(tweet.id["value"], tweet.text["value"], tweet.created_at["value"], tweet.last_updated["value"], tweet.times["value"], tweet.image["value"]))
    else:
        for tweet in tweets:
            print(tweet)
        print(f"Total tweets: {len(tweets)}")
    return 0

def retrieve_tweet(db, id, csv):
    if not id:
        print("Error: ID is required for retrieve mode")
        return 1
    try:
        tweet = db.get_tweet(id)
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    if csv:
        print("id,text,created_at,last_updated,times,image")
        print("{},{},{},{},{},{}".format(tweet.id["value"], tweet.text["value"], tweet.created_at["value"], tweet.last_updated["value"], tweet.times["value"], tweet.image["value"]))
    else:
        print(tweet)
        if tweet.image["value"] is not None:
            # bolb to image
            type = tweet.image["value"][0:8]
            name = f"image_{tweet.id['value']}"
            if type == b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a":
                name += ".png"
            elif type == b"\xff\xd8\xff\xe0\x00\x10\x4a\x46":
                name += ".jpeg"
            elif type == b"GIF89a\xe5\x00":
                name += ".gif"
            file = open(f"{name}", "wb")
            image = tweet.image["value"]
            file.write(image)
            file.close()
            print(f"Image saved as {name}")
    return 0

def create_tweet(db, text, image_path):
    if not text:
        print("Error: Tweet is required for create mode")
        return 1
    if image_path:
        # check if image_path is valid
        if not image_path.endswith(".png") and not image_path.endswith(".jpeg") and not image_path.endswith(".gif") and not image_path.endswith(".PNG") and not image_path.endswith(".JPEG") and not image_path.endswith(".GIF") and not image_path.endswith(".jpg") and not image_path.endswith(".JPG") and not image_path.endswith(".jpg"):
            print("Error: Invalid image format. Supported formats: PNG, JPEG, GIF")
            return 1
        # image to bolb
        file = open(image_path, "rb")
        image = file.read()
        file.close()
    else:
        image = None

    try:
        model = TweetModel(text=text, image=image)
        db.add_tweet(model)
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0

def delete_tweet(db, id):
    if not id:
        print("Error: ID is required for delete mode")
        return 1
    try:
        db.delete_tweet(id)
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", type=str, required=False, default="list", help="Mode of operation. Available modes: list, retrieve, create, delete. Default is list.")
    parser.add_argument("-t", "--tweet", type=str, required=False, help="Tweet to create. Only used in create mode")
    parser.add_argument("-p", "--image_path", type=str, required=False, help="Path to image to attach to tweet. PNG, JPEG and GIF are supported. Only used in create mode")
    parser.add_argument("-i", "--id", type=str, required=False, help="ID of tweet to retrieve or delete. Only used in retrieve or delete mode")
    parser.add_argument("-l", "--limit", type=int, required=False, default=10, help="Limit of tweets to list. Only used in list mode. -1 for all tweets. Default is 10")
    parser.add_argument("-f", "--filter", type=str, required=False, help="Filter to apply to list of tweets. Contidition: field like %value%. Only used in list mode")
    parser.add_argument("-v","--verbose", "-v", action="store_true", help="Enable verbose mode")
    parser.add_argument("-n","--dry-run", action="store_true", help="Enable dry-run mode")
    parser.add_argument("-ver","--version", action="version", version="%(prog)s (version 0.1)")
    parser.add_argument("-csv","--csv", action="store_true", help="Enable csv output. Only used in list or retrieve mode")
    args = parser.parse_args()

    for arg in vars(args):
        if args.verbose:
            print(f"{arg}: {getattr(args, arg)}")

    print("-"*20)

    db = TweetDB()

    if args.mode == "list":
        ret = list_tweets(db, args.limit, args.filter, args.csv)
    elif args.mode == "retrieve":
        ret = retrieve_tweet(db, args.id, args.csv)
    elif args.mode == "create":
        ret = create_tweet(db, args.tweet, args.image_path)
    elif args.mode == "delete":
        ret = delete_tweet(db, args.id)
    else:
        print(f"Error: Invalid mode {args.mode}")
        exit(1)

    exit(ret)

if __name__ == "__main__":
    # main()

    db = TweetDB()

    db.drop_all_tables()
    db.create_all_tables()

    for i in range(40):
        model = TweetModel(text=f"Hello, world! {i}", image=None)
        db.add_tweet(model)

    ret = list_tweets(db, -1, None, False)
    print("-"*20)

    ret = retrieve_tweet(db, 5, False)

    print("-"*20)

    ret = create_tweet(db, "Hello, world!", "/workspace/server/tests/imgs/image.png")
    ret = create_tweet(db, "Hello, world!", "/workspace/server/tests/imgs/image.jpeg")
    ret = create_tweet(db, "Hello, world!", "/workspace/server/tests/imgs/image.gif")

    ret = list_tweets(db, -1, None, False)

    # ret = retrieve_tweet(db, 41, False)
    # ret = retrieve_tweet(db, 42, False)
    # ret = retrieve_tweet(db, 43, False)

    print("-"*20)

    ret = delete_tweet(db, 41)

    print("-"*20)


