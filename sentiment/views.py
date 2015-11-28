import json
from django.http import HttpResponse
from django.template import loader, RequestContext
from sentiment.models import SentimentAnalyzer


def index(request):
    template = loader.get_template('sentiment/index.html')
    return HttpResponse(template.render())


def analyze(request, q):
    return HttpResponse(SentimentAnalyzer.analyze(q))


def fetch(request):
    return HttpResponse(SentimentAnalyzer.fetch())


def stop(request):
    return HttpResponse(SentimentAnalyzer.stop())
