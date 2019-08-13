from flask import Flask
from twitter_stream.TweetStreamListener import Setup


app = Flask(__name__)

@app.route('/')
@app.route('/home')
def twitter_stream():
    tweet_stream = Setup()
    print(tweet_stream)
    return str(tweet_stream)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80, debug=True)


