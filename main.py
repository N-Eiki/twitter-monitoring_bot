#docker-compose run python3 python main.py
import tweepy
import textwrap
import os
import time
import requests
from dotenv import load_dotenv
load_dotenv()

# 反応したいキーワード（複数指定可）
keywords = [
  'test',
]


api_key = os.getenv('api_key')
api_secret = os.getenv('api_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')
line_notify_access_token = os.getenv('line_notify_access_token')
twitter_id = os.getenv('twitter_id')
class StreamListener(tweepy.Stream):
    # 対象のユーザーが新規にツイートをするたびにこの関数が走る
    def on_status(self, status):
        tweet_type = self.check_tweet_type(status)

        user = status.user.name
        text = status.text

        # 通常のツイート以外（リツイートやリプライ）だった場合はここで終了
        # if tweet_type != 'normal_tweet': return

        # ツイートの本文を取得（大文字/小文字の区別が面倒なのでとりあえず小文字に変換）
        text = status.text.lower()

        # ツイートの本文にキーワードが含まれているかどうかチェック
        
        #片方だけ含まれている場合
        url = "https://notify-api.line.me/api/notify"
        headers = {'Authorization': 'Bearer ' + line_notify_access_token}

        message = f'{user}さんのツイートを観測しました\n{text}'
        payload = {'message': message}
        r = requests.post(url, headers=headers, params=payload,)
        print('send to line')
        
    # ツイートの種類をチェック（リツイート or リプライ or 通常のツイート）
    def check_tweet_type(self, status):
        # JSON内のキーに「retweeted_status」があればリツイート
        if 'retweeted_status' in status._json.keys():
            return 'retweet'

        # 「in_reply_to_user_id」がNoneでなかった場合はリプライ
        elif status.in_reply_to_user_id != None:
            return 'reply'

        # それ以外は通常のツイート
        else:
            return 'normal_tweet'

# 各認証情報を準備


if __name__=="__main__":
    # リスナーを作成
    stream_listener = StreamListener(consumer_key=api_key, consumer_secret=api_secret, access_token=access_token, access_token_secret=access_token_secret)

    # 監視対象のユーザーIDを調べる（https://idtwi.com/)
    twitter_user_id = [twitter_id] 
    # 監視スタート
    print('Start watching tweets')

    # ユーザーIDは配列で複数渡す事が可能
    # もし別のスレッドで非同期処理を行わせたい場合はfilterの引数に「is_async = True」を渡す
    stream_listener.filter(follow=twitter_user_id,)
