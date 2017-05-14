from django.conf.urls import url
from django.views.generic import TemplateView

from django.contrib import admin
from . import views

urlpatterns = [
 	url(r'^v1$',         views.api,      	 name='api'),
    url(r'^v1/games$',     views.games,      name='allgames'),
    url(r'^v1/stats$',     views.stats,      name='stats'),
    url(r'^v1/highscores$',views.highscores, name='highscores'),
]
#Names need clearn up, just for consistence view
