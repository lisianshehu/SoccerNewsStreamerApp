from flask import Flask, escape, request
from TweetStreamListener import Setup
from test import Test

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def twitter_stream():
    tweet_stream = Setup()
    return str(tweet_stream)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80, debug=True)


