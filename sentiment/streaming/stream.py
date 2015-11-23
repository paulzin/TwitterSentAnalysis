import re
import threading

from urllib.error import HTTPError
from requests.packages.urllib3.exceptions import ProtocolError
from tweepy import Stream, Cursor, API
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from textblob import TextBlob

customer_key = "tiwHO5SbK7tHZdlHcS9mjtsOj"
customer_secret = "r8nOaHsTN4mD7ORAp7w4XJbV3MglPvUxN66gys03jP6yTLWi3E"
access_token = "1011743515-3FNwAjIlBlzMXdUKU9mdEPCaW0UaFo0YB1CknZr"
access_secret = "yifgUgEY00Y2sxqlX0X0mq2Av2nXcGXvsHCwt8btn7Qdr"

pos_tweets = []
neg_tweets = []
twitter_stream = None

class TweetsStreamListener(StreamListener):
    def on_status(self, status):
        tweet = TextBlob(re.sub(r"http\S+", "", status.text))

        if len(tweet) < 4:
            return

        if tweet.detect_language() == 'en':
            result = str(tweet + " [" + str(tweet.polarity) + "]")

            if tweet.polarity >= 0.7:
                pos_tweets.append(str(tweet))
                print("POSITIVE: " + result)
            if tweet.polarity <= -0.5:
                neg_tweets.append(str(tweet))
                print("NEGATIVE: " + result)

    def on_error(self, status_code):
        print(str(status_code))


auth = OAuthHandler(customer_key, customer_secret)
auth.set_access_token(access_token, access_secret)


def get_live_tweets(query):
    while True:
        try:
            print("Streaming started")
            global twitter_stream
            global pos_tweets
            global neg_tweets
            if twitter_stream is not None:
                twitter_stream.disconnect()
                pos_tweets = []
                neg_tweets = []

            twitter_stream = Stream(auth, TweetsStreamListener())
            twitter_stream.filter(track=query)
        except ProtocolError:
            print("ProtocolError: restarting stream...")
            continue
        except HTTPError as e:
            print(e)
            continue


def get_history(query):
    api = API(auth)
    for status in Cursor(api.search, q=query, language='en').items(50):
        tweet = TextBlob(re.sub(r"http\S+", "", status.text))

        if len(tweet) < 4:
            return

        if tweet.detect_language() == 'en':
            result = str(tweet + " [" + str(tweet.polarity) + "]")

            if tweet.polarity >= 0.7:
                pos_tweets.append(str(tweet))
                print("POSITIVE: " + result)
            if tweet.polarity <= -0.5:
                neg_tweets.append(str(tweet))
                print("NEGATIVE: " + result)

    get_live_tweets(query)


def start(query):
    get_history(query)
