from django.conf.urls import patterns, url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^socialnetwork/', include('socialnetwork.urls')),
    url(r'^$', 'socialnetwork.views.home'),
]
