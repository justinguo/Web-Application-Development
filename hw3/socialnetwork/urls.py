from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'socialnetwork.views.home', name='home'),
    url(r'^add-post', 'socialnetwork.views.add_post', name='add'),
    url(r'^profile/(?P<id>\d+)$', 'socialnetwork.views.user_post', name='profile'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'socialnetwork/login.html'}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^register$', 'socialnetwork.views.register', name='register'),
]
