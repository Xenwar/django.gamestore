from django.conf.urls import url
from django.views.generic import TemplateView

from django.contrib import admin
from .views import error_to_game, score_from_game,setting_from_game,save_from_game,loadrequest_from_game

urlpatterns = [
    #MMessaging urls
    #url(r'^loadstate/([0-9]+)/$', load_state_to_game, name="loadstate"),
    url(r'^loaderror/(?P<gamename>[\w\-]+)/$',    error_to_game,        name="loaderror"   ),
    url(r'^savescore/(?P<gamename>[\w\-]+)/$',    score_from_game,      name="savescore"   ),
    url(r'^loadsetting/(?P<gamename>[\w\-]+)/$',  setting_from_game,    name="loadsetting" ),
    url(r'^savestate/(?P<gamename>[\w\-]+)/$',    save_from_game,       name="savestate"   ),
    url(r'^loadrequeset/(?P<gamename>[\w\-]+)/$', loadrequest_from_game,name="loadrequeset"),
]
#Names need clearn up, just for consistence view
