from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include

urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^members/'   , include('members.urls')),
        url(r'^gamesite/'  , include('gamesite.urls')),
        url(r'^gamecenter/', include('gamecenter.urls')),
        url(r'^messaging/' , include('messaging.urls')),
        url(r'^utilities/' , include('utilities.urls')),
		url(r'^api/' , include('api.urls')),
        url(r'^$^', RedirectView.as_view(url='/gamesite/', permanent=True)),
        url('^accounts/', include('django.contrib.auth.urls')),
        url('', include('social_django.urls', namespace='social'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)