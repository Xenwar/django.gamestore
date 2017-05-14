from django.conf.urls import url
from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib import admin
from . import views
from .views import register, logging_in,logging_out,activation,developer_games,player_games
from .views import addgame, updategame, GameListView, GameDetailView, deletegame, play_game_view,purchase_game, \
payment_success,payment_error,payment_cancel
urlpatterns = [
    url(r'^addgame/$',addgame,name='addgame'),
    url(r'^games/$', views.GameListView.as_view(),name='games'),
    #url(r'^search/(?P<game_name>[\w\-]+)/$', views.GameSearchView.as_view(),name='search'),

    url(r'^updategame/(?P<game_name>[\w\-]+)/$',updategame,name="updategame"),
    url(r'^deletegame/(?P<game_name>[\w\-]+)/$',deletegame,name="deletegame"),

    url(r'^developergames',    developer_games,   name='developergames'),
    url(r'^playergames',       player_games,      name='playergames'),

    #url(r'^playgame/([0-9]+)/$',play_game_view, name='playgame'),
    url(r'^game/(?P<pk>\d+)$',views.GameDetailView.as_view(),name='game-detail'),
    url(r'^playgame/(?P<game_name>[\w\-]+)/$',    play_game_view,name="playgame"   ),



    url(r'^purchase/(?P<game_name>[\w\-]+)/$', purchase_game,name="purchase"),
    url(r'^testgame/', TemplateView.as_view(template_name="gamecenter/teachers_example_game.html"),name='testgame'),
    url(r'^testgame/', TemplateView.as_view(template_name="gamesite/sampleGame.html"),name='testgame'),

    url(r'^paysuccess',  payment_success, name='paysuccess'),
    url(r'^payerror/$'  ,payment_error,   name='payerror'),
    url(r'^paycancel/$', payment_cancel,  name='paycancel'),
]
#Names need clearn up, just for consistence view
