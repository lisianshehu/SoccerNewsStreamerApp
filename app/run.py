from gevent import monkey
monkey.patch_all()
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from tweepy import OAuthHandler, API
from twitter_stream.config import *
from flask_socketio import SocketIO, emit, send, Namespace
from tweepy import StreamListener, Stream
import logging
import json

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.static_folder = 'static'
socketio = SocketIO(app, async=True)

@app.route('/')
@app.route('/home')
def twitter_stream():
    with app.app_context():
        return render_template('home.html')

class TweetStreamListener(StreamListener):

    def __init__(self):
        self.all_ids = []
        self.all_tweets = []

    def on_data(self, data):
        payload = json.loads(data)
        decoded_data = json.dumps(payload, indent=4, sort_keys=True)
        # print(decoded_data)
        if payload["user"]["verified"] is True or payload["user"]["followers_count"] > 100000:
            tweet_id = payload["id"]
            user = payload["user"]["screen_name"]
            tweet = payload["text"]
            if self.check_for_duplicates(tweet_id, tweet) and self.filter(tweet):
                tweet_data = user + tweet
                logging.info(tweet_data + "\n")
                self.send_tweet(tweet_data)
                # print(tweet_data)
            # else:
                # self.send_tweet("Duplicate")


    def filter(self, tweet):
        # print("This is the tweet that is being filtered: " + tweet)
        if tweet.find("bet") == -1:
            # logging.debug("Tweet is valid")
            return True
        else:
            # logging.debug("Tweet is invalid")
            return False

    def check_for_duplicates(self, tweet_id, tweet_text) -> bool:
        if tweet_id not in self.all_ids and tweet_text not in self.all_tweets:
            # logging.info("Tweet not seen before, adding to the list")
            self.all_ids.append(tweet_id)
            print("tweet id: " + str(tweet_id))
            print("checking tweet")
            self.all_tweets.append(tweet_text)
            print(self.all_ids)
            return True
        else:
            # logging.info("Tweet has been seen before")
            return False

    def get_link(self, tweet):
        tweet = str(tweet)
        if tweet.find('https') != -1:
            tweet_list = tweet.split('https:')
            temp_link = tweet_list[1]
            raw_tweet = tweet_list[0]
            link = 'https:' + temp_link
            # print("Link " + link)
            tweet_payload = {'tweet': raw_tweet, 'tweet_link': link}
            return tweet_payload
        else:
            tweet_payload = {'tweet': tweet, 'tweet_link': ""}
            return tweet_payload


    def send_tweet(self, tweet):
        print("trying to pass tweet")
        tweet_payload = self.get_link(tweet)
        Sock().tweet_received(tweet_payload)

    def on_status(self, status):
        print(status.text)

    def on_error(self, status):
        print(status)


class Sock:

    @staticmethod
    @socketio.on('my event')
    def connect(text):
        listener = TweetStreamListener()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = API(auth)
        stream = Stream(auth, listener)
        stream.filter(track=["soccer transfer", "transfer news", "premier league", "liverpool", "manchester united"], is_async=True,
                      languages=["en"])
        logging.basicConfig(filename="tweet_stream.log", level=logging.DEBUG)
        logging.info("Streaming Soccer Related Tweets\n")
        print(text)

    # @staticmethod
    # @socketio.on('my event2')
    # def test_tweet(json):
    #     print("Recieved: " + str(json))
    #     emit('stinky', json)

    @staticmethod
    @socketio.on('my event1')
    def tweet_received(tweet_payload: dict):
        # text = str(text)
        print("Tweet " + tweet_payload.get('tweet'))
        print("Link " + tweet_payload.get('tweet_link'))
        socketio.emit('tweet_response', tweet_payload, broadcast=True, namespace='/')





if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0',port=80, debug=True)


