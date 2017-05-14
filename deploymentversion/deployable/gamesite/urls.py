from django.conf.urls import url
from django.views.generic import TemplateView

from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.index, name='index'),
]
#Names need clearn up, just for consistence view
