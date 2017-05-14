from django.conf.urls import url
from django.views.generic import TemplateView

from django.contrib import admin
from . import views

urlpatterns = [
 	url(r'v1',         views.api,      	 name='api'),
    url(r'^games',     views.games,      name='games'),
    url(r'^stats',     views.stats,      name='stats'),
    url(r'^highscores',views.highscores, name='highscores'),
]
#Names need clearn up, just for consistence view
