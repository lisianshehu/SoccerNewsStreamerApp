import json
from tweepy.streaming import StreamListener, Stream
from tweepy import OAuthHandler, API
from elasticsearch import Elasticsearch
from twitter_stream.config import *
import logging
import app.run

es = Elasticsearch()


class Setup():

    def __init__(self):
        listener = TweetStreamListener()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = API(auth)
        stream = Stream(auth, listener)
        stream.filter(track=["soccer transfer", "transfer news", "premier league", "liverpool"], is_async=True, languages=["en"])
        logging.basicConfig(filename="tweet_stream.log", level=logging.DEBUG)
        logging.info("Streaming Soccer Related Tweets\n")


class TweetStreamListener(StreamListener):

    def __init__(self):
        self.all_ids = []

    def on_data(self, data):
        payload = json.loads(data)
        decoded_data = json.dumps(payload, indent=4, sort_keys=True)
        # print(decoded_data)
        if payload["user"]["verified"] is True or payload["user"]["followers_count"] > 100000:
            tweet_id = payload["id"]
            user = payload["user"]["screen_name"]
            tweet = payload["text"]
            if self.check_for_duplicates(tweet_id) and self.filter(tweet):
                tweet_data = user + tweet
                logging.info(tweet_data + "\n")
                self.send_tweet(tweet_data)
                print(tweet_data)


    def filter(self, tweet):
        # print("This is the tweet that is being filtered: " + tweet)
        if tweet.find("bet") == -1:
            # logging.debug("Tweet is valid")
            return True
        else:
            # logging.debug("Tweet is invalid")
            return False

    def check_for_duplicates(self, tweet_id) -> bool:
        if tweet_id not in self.all_ids:
            # logging.info("Tweet not seen before, adding to the list")
            self.all_ids.append(tweet_id)
            return True
        else:
            # logging.info("Tweet has been seen before")
            return False

    def send_tweet(self, tweet):
        return tweet

    def on_status(self, status):
        print(status.text)
        app.run.tweet_recieved(status.text)

    def on_error(self, status):
        print(status)
