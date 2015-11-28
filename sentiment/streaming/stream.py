import re
from urllib.error import HTTPError

from requests.packages.urllib3.exceptions import ProtocolError
from textblob import TextBlob
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

customer_key = "tiwHO5SbK7tHZdlHcS9mjtsOj"
customer_secret = "r8nOaHsTN4mD7ORAp7w4XJbV3MglPvUxN66gys03jP6yTLWi3E"
access_token = "1011743515-3FNwAjIlBlzMXdUKU9mdEPCaW0UaFo0YB1CknZr"
access_secret = "yifgUgEY00Y2sxqlX0X0mq2Av2nXcGXvsHCwt8btn7Qdr"

POS_PARAM = 0.7
NEG_PARAM = -0.5

pos_tweets = []
neg_tweets = []
twitter_stream = None

is_streaming = False


class TweetsStreamListener(StreamListener):
    def on_status(self, status):
        tweet = TextBlob(re.sub(r"http\S+", "", status.text))

        if len(tweet) < 4:
            return

        if tweet.detect_language() == 'en':
            result = str(tweet + " [" + str(tweet.polarity) + "]")

            tweet_text = str(tweet)
            if tweet.polarity >= POS_PARAM and tweet_text not in pos_tweets:
                pos_tweets.append(tweet_text)
                print("POSITIVE: " + result)
            if tweet.polarity <= NEG_PARAM and tweet_text not in neg_tweets:
                neg_tweets.append(tweet_text)
                print("NEGATIVE: " + result)

    def on_error(self, status_code):
        print(str(status_code))


auth = OAuthHandler(customer_key, customer_secret)
auth.set_access_token(access_token, access_secret)


def get_live_tweets(query):
    global is_streaming

    while is_streaming:
        try:
            print("Streaming started")
            global twitter_stream
            global pos_tweets
            global neg_tweets

            twitter_stream = Stream(auth, TweetsStreamListener())
            twitter_stream.filter(track=[query])
        except ProtocolError:
            print("ProtocolError: restarting stream...")
            continue
        except HTTPError as e:
            print("HTTPError:", e)
            continue


def start(query):
    global is_streaming
    is_streaming = True
    get_live_tweets(query)


def stop():
    global twitter_stream, pos_tweets, neg_tweets, is_streaming
    if twitter_stream:
        is_streaming = False
        print("Streaming stopped")
        twitter_stream.disconnect()
        pos_tweets = []
        neg_tweets = []
