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
usage: main.py [-h] [-o] [-i INTERVAL] [-ri RANDOM_INTERVAL] [-bt BEARER_TOKEN] [-ak API_KEY] [-aks API_KEY_SECRET] [-at ACCESS_TOKEN] [-ats ACCESS_TOKEN_SECRET] [-ver] [-v] [-q] [-n] [-s SEED] [-en]
               [-es EMAIL_SERVER] [-ep EMAIL_PORT] [-ef EMAIL_FROM] [-ps EMAIL_PASSWORD] [-et EMAIL_TO] [-su EMAIL_SUBJECT] [-bo EMAIL_BODY] [-etest] [-on]

optional arguments:
  -h, --help            show this help message and exit
  -o, --onetweet        Only tweet once and exit
  -i INTERVAL, --interval INTERVAL
                        Interval in seconds between tweets. Default is 3 hours
  -ri RANDOM_INTERVAL, --random_interval RANDOM_INTERVAL
                        Random interval in seconds between tweets. Default is 0. If set, interval is used as the maximum value
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
  -etest, --email_test
                        Enable email test
  -on, --only_new
                        Only tweet new tweets
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

## ツイートデータの操作

ツイートデータはデータベースに保存されます。
データベースの操作には、`utils.py`を使用します。

```bash
python utils.py
```

`-h` オプションでヘルプを表示できます。

```bash
usage: utils.py [-h] [-m MODE] [-t TWEET] [-p IMAGE_PATH] [-i ID] [-l LIMIT] [-f FILTER] [-v] [-n] [-ver] [-csv]

optional arguments:
  -h, --help            show this help message and exit
  -m MODE, --mode MODE  Mode of operation. Available modes: list, retrieve, create, delete, backup, restore. Default is list.
  -t TWEET, --tweet TWEET
                        Tweet to create. Only used in create mode
  -p IMAGE_PATH, --image_path IMAGE_PATH
                        Path to image to attach to tweet. PNG, JPEG and GIF are supported. Only used in create mode
  -i ID, --id ID        ID of tweet to retrieve or delete. Only used in retrieve or delete mode
  -l LIMIT, --limit LIMIT
                        Limit of tweets to list. Only used in list mode. -1 for all tweets. Default is 10
  -f FILTER, --filter FILTER
                        Filter to apply to list of tweets. Contidition: field like %value%. Only used in list mode
  -v, --verbose         Enable verbose mode
  -n, --dry-run         Enable dry-run mode
  -ver, --version       show program's version number and exit
  -csv, --csv           Enable csv output. Only used in list or retrieve mode
  -db, --db_file        Database file name. Only used in backup or restore mode. Default is from environment variable DB_FILE
  -bdb, --backup_db_file
                        Backup database file name. Only used in backup or restore mode.
```

## ツイートの一覧表示

`list`モードでツイートの一覧を表示できます。

```bash
python utils.py -m list
```

`-l` オプションで表示するツイートの数を指定できます。

```bash
python utils.py -m list -l 5
```

`-f` オプションで表示するツイートを絞り込むことができます。

```bash
python utils.py -m list -f "hoge"
```

`-csv` オプションでCSV形式で出力できます。

```bash
python utils.py -m list -csv
```

## ツイートの取得

`retrieve`モードでツイートを取得できます。

```bash
python utils.py -m retrieve -i 1
```

`-csv` オプションでCSV形式で出力できます。

```bash
python utils.py -m retrieve -i 1 -csv
```

## ツイートの登録

`create`モードでツイートを登録できます。

```bash
python utils.py -m create -t "hoge"
```

`-p` オプションで画像を添付できます。

```bash
python utils.py -m create -t "hoge" -p "path/to/image.png"
```

改行を含むツイートを登録する場合は、クォーテーションの前に$を付けて\nで改行してください。

```bash
python utils.py -m create -t $'hoge\nfuga'
```

## ツイートの更新

TODO

## ツイートの削除

`delete`モードでツイートを削除できます。

```bash
python utils.py -m delete -i 1
```

## データベースのバックアップ

`backup`モードでデータベースをバックアップできます。

```bash
python utils.py -m backup -bdb "backup.db"
```

## データベースのリストア

`restore`モードでデータベースをリストアできます。

```bash
python utils.py -m restore -bdb "backup.db"
```

## Dockerで使用する

Dockerで使用する場合は、以下のようにします。
DockerHubからイメージを取得するか、このリポジトリをクローンしてビルドしてください。
[DockerHub-ray_x_bot](https://hub.docker.com/r/kchihogi/ray_x_bot "DockerHub")はこちら。

ディレクトリの作成と移動

```bash
mkdir ray_x_bot
cd ray_x_bot
```

.envファイルを作成

```bash
touch .env
```

.envファイルに環境変数を設定

```bash
API_KEY=
API_KEY_SECRET=
BEARER_TOKEN=
ACCESS_TOKEN=
ACCESS_TOKEN_SECRET=
CLIENT_ID=
CLIENT_SECRET=
REDIRECT_URI=
EMAIL_SERVER=
EMAIL_PORT=
EMAIL_FROM=
EMAIL_PASSWORD=
EMAIL_TO=
EMAIL_SUBJECT=
EMAIL_BODY=
DB_FILE=
```

Dockerイメージを取得

```bash
docker pull kchihogi/ray_x_bot
```

または、このリポジトリをクローンしてビルド

```bash
git clone
docker build -t ray_x_bot .
```

Dockerコンテナを起動

```bash
docker run -d --env-file .env --name ray_x_bot ray_x_bot python /usr/local/server/main.py
```

Dockerコンテナを停止

```bash
docker stop ray_x_bot
```

Dockerコンテナを再起動

```bash
docker start ray_x_bot
```

Dockerコンテナを削除

```bash
docker rm ray_x_bot
```

Dockerイメージを削除

```bash
docker rmi ray_x_bot
```

Dockerコンテナへアタッチ
DB操作はutils.pyを使用してください。
utils.pyはDockerコンテナ内にインストールされています。
/usr/local/server/utils.pyを実行する

```bash
docker exec -it ray_x_bot /usr/local/server/utils.py
```

## ライセンス

MIT

