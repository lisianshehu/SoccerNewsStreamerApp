from gevent import monkey
monkey.patch_all()
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from tweepy import OAuthHandler
from flask_socketio import SocketIO
from tweepy import StreamListener, Stream
import logging
import json
import os
from dotenv import load_dotenv

app = Flask(__name__, static_folder='static', template_folder='templates')
bootstrap = Bootstrap(app)
socketio = SocketIO(app)


@app.route('/')
@app.route('/home')
def twitter_stream():
    with app.app_context():
        return render_template('news_stream.html')


class TweetStreamListener(StreamListener):

    def __init__(self):
        self.all_ids = set()
        self.all_tweets = set()

    def on_data(self, data):
        payload = json.loads(data)
        try:
            if payload["user"]["verified"] is True or payload["user"]["followers_count"] > 100000:
                tweet_id = payload["id"]
                user = payload["user"]["screen_name"]
                tweet = payload["text"]
                if self.check_for_duplicates(tweet_id, tweet) and self.filter(tweet):
                    tweet_data = user + tweet
                    logging.info(tweet_data + "\n")
                    self.send_tweet(tweet_data)
        except KeyError:
            logging.warn('Could not find user field in tweet data')

    def filter(self, tweet):
        if tweet.find("bet") == -1:
            return True
        else:
            return False

    def check_for_duplicates(self, tweet_id, tweet_text) -> bool:
        if tweet_id not in self.all_ids and tweet_text not in self.all_tweets:
            logging.info('Checking duplicate tweet_id: {}'.format(tweet_id))
            self.all_ids.add(tweet_id)
            self.all_tweets.add(tweet_text)
            return True
        else:
            return False

    def get_link(self, tweet):
        tweet = str(tweet)
        if tweet.find('https') != -1:
            tweet_list = tweet.split('https:')
            temp_link = tweet_list[1]
            raw_tweet = tweet_list[0]
            link = 'https:' + temp_link
            tweet_payload = {'tweet': raw_tweet, 'tweet_link': link}
            return tweet_payload
        else:
            tweet_payload = {'tweet': tweet, 'tweet_link': ""}
            return tweet_payload

    def send_tweet(self, tweet):
        tweet_payload = self.get_link(tweet)
        Sock().tweet_received(tweet_payload)

    def on_status(self, status):
        logging.info(status.text)

    def on_error(self, status):
        logging.error(status)


class Sock:

    @staticmethod
    @socketio.on('connected')
    def connect(text):
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        consumer_key = os.environ.get('CONSUMER_KEY')
        consumer_secret = os.environ.get('CONSUMER_SECRET')
        access_token = os.environ.get('ACCESS_TOKEN')
        access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')
        keyword_list = os.environ.get('KEYWORD_LIST').split(',')

        listener = TweetStreamListener()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, listener)
        stream.filter(track=keyword_list, is_async=True,
                      languages=["en"])
        logging.basicConfig(filename="tweet_stream.log", level=logging.DEBUG)
        logging.info("Streaming Soccer Related Tweets\n")

    @staticmethod
    @socketio.on('my event1')
    def tweet_received(tweet_payload: dict):
        logging.info("Tweet " + tweet_payload.get('tweet'))
        logging.info("Link " + tweet_payload.get('tweet_link'))
        socketio.emit('tweet_response', tweet_payload, broadcast=True, namespace='/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


