from django.conf.urls import url
from django.conf.urls import url
from django.views.generic import TemplateView

from django.contrib import admin
from . import views
from .views import register, logging_in,logging_out,activation

urlpatterns = [
    #Related to account holder, both developers and players
    url(r'^members/$',views.MemberListView.as_view(),             name='members'),
    #url(r'^member/(?P<pk>\d+)$',views.MemberDetailView.as_view(), name='member-detail'),

    #url(r'^members/$', developers_list,name="members"),
    
    url(r'^players/$',          views.PlayerListView.as_view(),   name='players'),
    #url(r'^player/(?P<pk>\d+)$',views.PlayerDetailView.as_view(), name='state-detail'),
    url(r'^register/$',  register, name="register"),
    url(r'^login/$',   logging_in, name="loggin_in"),
    url(r'^logout/$', logging_out, name="loggin_out"),
    url(r'^activate/$',activation, name="activation"),

]
#Names need clearn up, just for consistence view
