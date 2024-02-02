import argparse
import os
import time
import tweepy
from randomizer import Randomizer

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--onetweet", action="store_true", help="Only tweet once and exit")
    parser.add_argument("-i", "--interval", type=int, required=False, default=(60*60*3), help="Interval in seconds between tweets. Default is 3 hours")
    parser.add_argument("-bt", "--bearer_token", type=str, required=False, default=os.environ['BEARER_TOKEN'], help="Bearer token for Twitter API")
    parser.add_argument("-ak","--api_key", type=str, required=False, default=os.environ['API_KEY'], help="API key for Twitter API")
    parser.add_argument("-aks","--api_key_secret", type=str, required=False, default=os.environ['API_KEY_SECRET'], help="API key secret for Twitter API")
    parser.add_argument("-at","--access_token", type=str, required=False, default=os.environ['ACCESS_TOKEN'], help="Access token for Twitter API")
    parser.add_argument("-ats","--access_token_secret", type=str, required=False, default=os.environ['ACCESS_TOKEN_SECRET'], help="Access token secret for Twitter API")
    parser.add_argument("-ver","--version", action="version", version="%(prog)s (version 0.1)")
    parser.add_argument("-v","--verbose", "-v", action="store_true", help="Enable verbose mode")
    parser.add_argument("-q","--quiet", "-q", action="store_true", help="Enable quiet mode")
    parser.add_argument("-n","--dry-run", action="store_true", help="Enable dry-run mode")
    args = parser.parse_args()

    for arg in vars(args):
        if not args.quiet and args.verbose:
            print(f"{arg}: {getattr(args, arg)}")

    client = tweepy.Client(
        consumer_key=args.api_key,
        consumer_secret=args.api_key_secret,
        access_token=args.access_token,
        access_token_secret=args.access_token_secret
    )

    randomizer = Randomizer() # db connection in Randomizer

    if args.onetweet:
        if not args.quiet:
            print("Only tweeting once")
        tweet = randomizer.get_random_tweet()
        if args.dry_run:
            print("Dry-run mode enabled")
            print(f"Tweeting: {tweet}")
        else:
            client.create_tweet(text="Hello, world!")
        return
    else:
        if not args.quiet:
            print(f"Tweeting every {args.interval} seconds")
        try:
            while True:
                if not args.quiet:
                    print("Tweeting...")
                tweet = randomizer.get_random_tweet()
                if args.dry_run:
                    print("Dry-run mode enabled")
                    print(f"Tweeting: {tweet}")
                else:
                    client.create_tweet(text="Hello, world!")
                if not args.quiet:
                    print(f"Sleeping for 0 / {args.interval} seconds")
                cnt = 0
                while cnt < args.interval:
                    time.sleep(1)
                    cnt += 1
                    if cnt % (args.interval/10) == 0 and not args.quiet:
                        print(f"Sleeping for {cnt} / {args.interval} seconds")
        except KeyboardInterrupt:
            if not args.quiet:
                print("Exiting")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
