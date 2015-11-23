from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^analyze/(?P<q>[\s\S]{1,50})/$', views.analyze, name='analyze'),
    url(r'^fetch', views.fetch, name='fetch'),
]
