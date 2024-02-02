# ray_x_bot
RAY Xボット(非公式)

## 使い方

1. このリポジトリをクローンします。
2. `pip install -r requirements.txt` を実行します。
3. `python main.py` を実行します。

```bash
git clone
pip install -r requirements.txt
python main.py
```

`-h` オプションでヘルプを表示できます。

```bash
usage: main.py [-h] [-o] [-i INTERVAL] [-bt BEARER_TOKEN] [-ak API_KEY] [-aks API_KEY_SECRET] [-at ACCESS_TOKEN] [-ats ACCESS_TOKEN_SECRET] [-ver] [-v] [-q] [-n] [-s SEED] [-en]
               [-es EMAIL_SERVER] [-ep EMAIL_PORT] [-ef EMAIL_FROM] [-ps EMAIL_PASSWORD] [-et EMAIL_TO] [-su EMAIL_SUBJECT] [-bo EMAIL_BODY] [-etest]

optional arguments:
  -h, --help            show this help message and exit
  -o, --onetweet        Only tweet once and exit
  -i INTERVAL, --interval INTERVAL
                        Interval in seconds between tweets. Default is 3 hours
  -bt BEARER_TOKEN, --bearer_token BEARER_TOKEN
                        Bearer token for Twitter API. Default is from environment variable BEARER_TOKEN
  -ak API_KEY, --api_key API_KEY
                        API key for Twitter API. Default is from environment variable API_KEY
  -aks API_KEY_SECRET, --api_key_secret API_KEY_SECRET
                        API key secret for Twitter API. Default is from environment variable API_KEY_SECRET
  -at ACCESS_TOKEN, --access_token ACCESS_TOKEN
                        Access token for Twitter API. Default is from environment variable ACCESS_TOKEN
  -ats ACCESS_TOKEN_SECRET, --access_token_secret ACCESS_TOKEN_SECRET
                        Access token secret for Twitter API. Default is from environment variable ACCESS_TOKEN_SECRET
  -ver, --version       show program's version number and exit
  -v, --verbose, -v     Enable verbose mode
  -q, --quiet, -q       Enable quiet mode
  -n, --dry-run         Enable dry-run mode
  -s SEED, --seed SEED  Seed for random number generator
  -en, --email_notification
                        Enable email notifications when failing to tweet
  -es EMAIL_SERVER, --email_server EMAIL_SERVER
                        Server of email to send. Default is from environment variable EMAIL_SERVER if set
  -ep EMAIL_PORT, --email_port EMAIL_PORT
                        Port of email to send. Default is from environment variable EMAIL_PORT if set
  -ef EMAIL_FROM, --email_from EMAIL_FROM
                        From of email to send. Default is from environment variable EMAIL_FROM if set
  -ps EMAIL_PASSWORD, --email_password EMAIL_PASSWORD
                        Password of email to send. Default is from environment variable EMAIL_PASSWORD if set
  -et EMAIL_TO, --email_to EMAIL_TO
                        To of email to send. Default is from environment variable EMAIL_TO if set
  -su EMAIL_SUBJECT, --email_subject EMAIL_SUBJECT
                        Subject of email to send. Default is from environment variable EMAIL_SUBJECT if set
  -bo EMAIL_BODY, --email_body EMAIL_BODY
                        Body of email to send. Default is from environment variable EMAIL_BODY if set
  -etest, --email_test  Enable email test
```

## 環境変数

以下の環境変数を設定することで、コマンドラインオプションを省略できます

- `BEARER_TOKEN`: Twitter APIのBearerトークン
- `API_KEY`: Twitter APIのAPIキー
- `API_KEY_SECRET`: Twitter APIのAPIキーシークレット
- `ACCESS_TOKEN`: Twitter APIのアクセストークン
- `ACCESS_TOKEN_SECRET`: Twitter APIのアクセストークンシークレット
- `CLIENT_ID`: Twitter APIのクライアントID
- `CLIENT_SECRET`: Twitter APIのクライアントシークレット
- `REDIRECT_URI`: Twitter APIのリダイレクトURI
- `EMAIL_SERVER`: 通知用メールのサーバー
- `EMAIL_PORT`: 通知用メールのポート
- `EMAIL_FROM`: 通知用メールの送信元
- `EMAIL_PASSWORD`: 通知用メールのパスワード
- `EMAIL_TO`: 通知用メールの送信先
- `EMAIL_SUBJECT`: 通知用メールの件名
- `EMAIL_BODY`: 通知用メールの本文
- `DB_FILE`: データベースファイル名

## データベース

データベースはSQLite3を使用しています。デフォルトでは`ray_x_bot.db`というファイル名で保存されます。
環境変数`DB_FILE`のみでファイル名を変更できます。

## ツイートの登録

TODO

## ツイートの削除

TODO

## ツイートの一覧表示

TODO

## ライセンス

MIT

