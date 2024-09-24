import argparse
import asyncio
import aioconsole
import os
import time
from datetime import datetime, timedelta
import tweepy
from randomizer import Randomizer
from mailer import Mailer

def upload_image(tweet, api):

    if tweet.image["value"] is None:
        raise Exception("No image to upload")
    
    id = tweet.id["value"]
    blob = tweet.image["value"]

    filename = "image_" + str(id)
    media_category = "" # tweet_image, tweet_video, tweet_gif

    type = blob[0:8]
    if type == b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a":
        filename += ".png"
        media_category = "tweet_image"
    elif type == b"\xff\xd8\xff\xe0\x00\x10\x4a\x46":
        filename += ".jpeg"
        media_category = "tweet_image"
    elif type == b"GIF89a\xe5\x00":
        filename += ".gif"
        media_category = "tweet_gif"
    else:
        raise Exception("Unsupported image type")
    
    if os.path.exists(filename):
        os.remove(filename)

    with open(filename, "wb") as file:
        file.write(blob)

    media = api.media_upload(filename=filename, media_category=media_category, chunked=True)
    os.remove(filename)

    return [media.media_id]

def tweet(args, randomizer, client, api):
    ret = 0
    try:
        tweet = randomizer.get_random_tweet(args.only_new, args.dry_run)
        if args.dry_run:
            print("Dry-run mode enabled")
            print(f"Tweeting: {tweet}")
        else:
            if tweet.image["value"] is not None:
                media_ids = upload_image(tweet, api)
                client.create_tweet(text=tweet.text["value"], media_ids=media_ids)
            else:
                client.create_tweet(text=tweet.text["value"])
        ret = 0
    except ValueError as e:
        # no tweets found is ignored
        if not args.quiet:
            print(f"WARN: {e}")
        ret = 0
    except Exception as e:
        if args.email_notification:
            if not args.quiet:
                print(f"Sending email notification")
            # send email
            mailer = Mailer(args.email_from, args.email_password, args.email_server, args.email_port, args.diable_check_ssl)
            body = args.email_body + f"\nError: {e}"
            mailer.send_email(args.email_to, args.email_subject, body)
        print(f"Error: {e}")
        ret = 1
    return ret

async def check_for_skip():
    """非同期でユーザーが'S'を押すかを確認"""
    while True:
        print("Press 'S' to skip next tweet.")
        try:
            user_input = await aioconsole.ainput()
            if user_input.lower() == 's':
                print("Skipping next tweet!")
                return True
            else:
                print(f"Invalid input: {user_input}. Press 'S' to skip the next tweet.")
                return False
        except EOFError:
            print("No input provided. Exiting the check.")
            return False
        except Exception as e:
            print(f"Error occurred. Exiting the check. Error: {e}")
            return False

async def wait_for_tweet(args, randomizer, previous_interval):
    interval = args.interval
    base_interval = args.interval
    diff = base_interval - previous_interval if previous_interval > 0 else 0

    if args.random_interval > 0:
        interval = randomizer.generate_random_number(args.random_interval, base_interval)

    if diff > 0:
        if not args.quiet:
            print(f"Sleeping for {diff} seconds to compensate for previous tweet")
        time.sleep(diff)

    if not args.quiet:
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        now_plus_interval = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + interval))
        print(f"Sleeping for 0 / {interval} seconds. Current time: {now}. Next tweet at: {now_plus_interval}")

    input_task = asyncio.create_task(check_for_skip())
    
    if not args.quiet and args.verbose:
        print("Creating input task to check for 'S' input")

    cnt = 0
    skip = False
    while cnt < interval:
        sleep_task = asyncio.create_task(asyncio.sleep(1))

        if not args.quiet and args.verbose:
            print(f"Creating task to sleep for 1 second. Current count: {cnt}")

        if skip:
            done, pending = await asyncio.wait([sleep_task], return_when=asyncio.FIRST_COMPLETED)
        else:
            done, pending = await asyncio.wait([input_task, sleep_task], return_when=asyncio.FIRST_COMPLETED)

        if not args.quiet and args.verbose:
            print(f"Joining tasks. Current count: {cnt}. done: {done}. pending: {pending}")

        # sleep_taskが完了したらカウントを進める
        if sleep_task in done:
            cnt += 1

            if cnt % (interval // 10 if interval > 10 else 1) == 0 and not args.quiet:
                print(f"Sleeping for {cnt} / {interval} seconds")

        # 入力が完了していたらスキップフラグをセット
        if input_task in done:
            skip = await input_task  # 'S'が押されたか確認
            if not skip:
                input_task.cancel()
                input_task = asyncio.create_task(check_for_skip())
    
    if not input_task.done():
        if not args.quiet and args.verbose:
            print("Cancelling input task")
        input_task.cancel()

    if skip:
        # reenter this function
        print("Skipping tweet by user request.")
        return await wait_for_tweet(args, randomizer, interval)

    return interval

def wait_until_specified_time(hour, minute):
    # 現在の時刻を取得
    now = datetime.now()

    # 今日の指定された時刻を設定
    target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

    # 現在の時刻が指定の時刻を過ぎている場合、翌日の指定時刻に設定
    if now > target_time:
        target_time += timedelta(days=1)

    # 指定時刻までの残り時間を計算
    time_to_wait = (target_time - now).total_seconds()

    print(f"Waiting for {time_to_wait // 3600:.0f} hours and {(time_to_wait % 3600) // 60:.0f} minutes and {time_to_wait % 60:.0f} seconds...")
    print(f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}. Waiting until: {target_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # 指定された時間まで待機
    time.sleep(time_to_wait)

    # 待機後の処理
    print("The specified time has arrived! Continuing process...")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--onetweet", action="store_true", help="Only tweet once and exit")
    parser.add_argument("-i", "--interval", type=int, required=False, default=(60*60*3), help="Interval in seconds between tweets. Default is 3 hours")
    parser.add_argument("-ri", "--random_interval", type=int, required=False, default=0, help="Random interval in seconds between tweets. Default is 0. If set, interval is used as the maximum value")
    parser.add_argument("-bt", "--bearer_token", type=str, required=False, default=os.environ['BEARER_TOKEN'], help="Bearer token for Twitter API. Default is from environment variable BEARER_TOKEN")
    parser.add_argument("-ak","--api_key", type=str, required=False, default=os.environ['API_KEY'], help="API key for Twitter API. Default is from environment variable API_KEY")
    parser.add_argument("-aks","--api_key_secret", type=str, required=False, default=os.environ['API_KEY_SECRET'], help="API key secret for Twitter API. Default is from environment variable API_KEY_SECRET")
    parser.add_argument("-at","--access_token", type=str, required=False, default=os.environ['ACCESS_TOKEN'], help="Access token for Twitter API. Default is from environment variable ACCESS_TOKEN")
    parser.add_argument("-ats","--access_token_secret", type=str, required=False, default=os.environ['ACCESS_TOKEN_SECRET'], help="Access token secret for Twitter API. Default is from environment variable ACCESS_TOKEN_SECRET")
    parser.add_argument("-ver","--version", action="version", version="%(prog)s (version 0.1)")
    parser.add_argument("-v","--verbose", action="store_true", help="Enable verbose mode")
    parser.add_argument("-q","--quiet", "-q", action="store_true", help="Enable quiet mode")
    parser.add_argument("-n","--dry-run", action="store_true", help="Enable dry-run mode")
    parser.add_argument("-s","--seed", type=int, required=False, help="Seed for random number generator")    
    parser.add_argument("-en","--email_notification", action="store_true", help="Enable email notifications when failing to tweet")
    parser.add_argument("-es","--email_server", type=str, required=False, default=os.environ['EMAIL_SERVER'] if 'EMAIL_SERVER' in os.environ else None, help="Server of email to send. Default is from environment variable EMAIL_SERVER if set")
    parser.add_argument("-ep","--email_port", type=int, required=False, default=os.environ['EMAIL_PORT'] if 'EMAIL_PORT' in os.environ else None, help="Port of email to send. Default is from environment variable EMAIL_PORT if set")
    parser.add_argument("-ef","--email_from", type=str, required=False, default=os.environ['EMAIL_FROM'] if 'EMAIL_FROM' in os.environ else None, help="From of email to send. Default is from environment variable EMAIL_FROM if set")
    parser.add_argument("-ps","--email_password", type=str, required=False, default=os.environ['EMAIL_PASSWORD'] if 'EMAIL_PASSWORD' in os.environ else None, help="Password of email to send. Default is from environment variable EMAIL_PASSWORD if set")
    parser.add_argument("-et","--email_to", type=str, required=False, default=os.environ['EMAIL_TO'] if 'EMAIL_TO' in os.environ else None, help="To of email to send. Default is from environment variable EMAIL_TO if set")
    parser.add_argument("-su","--email_subject", type=str, required=False, default=os.environ['EMAIL_SUBJECT'] if 'EMAIL_SUBJECT' in os.environ else None, help="Subject of email to send. Default is from environment variable EMAIL_SUBJECT if set")
    parser.add_argument("-bo","--email_body", type=str, required=False, default=os.environ['EMAIL_BODY'] if 'EMAIL_BODY' in os.environ else None, help="Body of email to send. Default is from environment variable EMAIL_BODY if set")
    parser.add_argument("-etest","--email_test", action="store_true", help="Enable email test")
    parser.add_argument("-on","--only_new", action="store_true", help="Only tweet new tweets")
    parser.add_argument("-ds","--diable_check_ssl", action="store_true", help="Disable SSL check for email")
    parser.add_argument("-sat","--start_datetime", type=str, required=False, help="Start datetime for tweeting. Format: HH:MM. Timezone is " + time.tzname[0] + "(" + time.strftime("%z", time.localtime()) + ").")
    args = parser.parse_args()

    if not args.quiet:
        print("=====Starting X RAY bot=====")

    for arg in vars(args):
        if not args.quiet and args.verbose:
            print(f"{arg}: {getattr(args, arg)}")

    if args.email_test:
        if not args.quiet:
            print("Sending test email")
        # send email
        mailer = Mailer(args.email_from, args.email_password, args.email_server, args.email_port, args.diable_check_ssl)
        mailer.send_email(args.email_to, args.email_subject, args.email_body)
        exit(0)

    auth = tweepy.OAuthHandler(args.api_key, args.api_key_secret)
    auth.set_access_token(args.access_token, args.access_token_secret)

    api = tweepy.API(auth)
    client = tweepy.Client(
        consumer_key=args.api_key,
        consumer_secret=args.api_key_secret,
        access_token=args.access_token,
        access_token_secret=args.access_token_secret
    )

    randomizer = Randomizer(args.seed) # db connection in Randomizer

    if args.onetweet:
        ret = tweet(args, randomizer, client, api)
        exit(ret)
    else:
        if not args.quiet:
            if args.random_interval > 0:
                print(f"Tweeting every {args.random_interval} - {args.interval} seconds")
            else:
                print(f"Tweeting every {args.interval} seconds")
        try:
            if args.start_datetime is not None:
                wait_until_specified_time((int(args.start_datetime.split(":")[0])), (int(args.start_datetime.split(":")[1])))
            previous_interval = 0
            while True:
                ret = tweet(args, randomizer, client, api)
                previous_interval = asyncio.run(wait_for_tweet(args, randomizer, previous_interval))
        except KeyboardInterrupt:
            if not args.quiet:
                print("Exiting")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
