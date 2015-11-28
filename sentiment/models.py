import threading

from django.db import models
from django.http import JsonResponse, HttpResponse
from .streaming import stream


class SentimentAnalyzer(models.Model):
    @staticmethod
    def analyze(tweet):
        thread = threading.Thread(target=stream.start, args=(tweet,))
        thread.start()
        return "It's ok!"

    @staticmethod
    def fetch():
        pos_count = len(stream.pos_tweets)
        neg_count = len(stream.neg_tweets)
        sum_count = pos_count + neg_count

        if not sum_count:
            return JsonResponse({"error": "Nothing fetched"})

        pos_percent = (pos_count * 100) / sum_count

        return JsonResponse({
            "pos": pos_percent,
            "neg": 100 - pos_percent,
            "last_pos_tweet": stream.pos_tweets[-1 if len(stream.pos_tweets) > 0 else None],
            "last_neg_tweet": stream.neg_tweets[-1 if len(stream.neg_tweets) > 0 else None],
            "pos_count": pos_count,
            "neg_count": neg_count
        })

    @staticmethod
    def stop():
        stream.stop()
        return HttpResponse("OK")


