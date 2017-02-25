from django.conf.urls import patterns, include, url
from socialnetwork.forms import LoginForm
from django.views.generic.base import TemplateView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
                       url(r'^$', 'socialnetwork.home_views.home', name='home'),
                       url(r'^followers$', 'socialnetwork.home_views.home_followers', name='home-followers'),
                       url(r'^register$', 'socialnetwork.register_views.register_user', name='register'),
                       url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', 
                           'socialnetwork.register_views.confirm_registration', name='confirm'),
                       url(r'^makepost-page$', 'socialnetwork.post_views.makepost_page', name='makepost-page'),
                       url(r'^make-a-post$', 'socialnetwork.post_views.make_a_post', name='make-a-post'),
                       url(r'^update-post/(?P<post_id>\d+)$', 'socialnetwork.post_views.update_posts', name='update-post'),
                       url(r'^follow/(?P<username>\w+)$', 'socialnetwork.buttons_views.follow', name='follow'),
                       url(r'^unfollow/(?P<username>\w+)$', 'socialnetwork.buttons_views.unfollow', name='unfollow'),
                       url(r'^edit-profile$', 'socialnetwork.profile_views.edit_profile', name='edit-profile'),
                       url(r'^edit-profile-img$', 'socialnetwork.profile_views.edit_profile_img',
                           name='edit-profile-img'),
                       url(r'^edit-profile-pw$', 'socialnetwork.profile_views.edit_profile_pw', name='edit-profile-pw'),
                       url(r'^edit-profile-info$', 'socialnetwork.profile_views.edit_profile_info',
                           name='edit-profile-info'),
                       url(r'^view-profile/(?P<view_user>\w+)$', 'socialnetwork.profile_views.view_profile_user',
                           name='view-profile-user'),
                       url(r'^get-comments/(?P<post_id>\d+)$', 'socialnetwork.comments_views.get_comments',
                           name='get-comments'),
                       url(r'^add-comment/(?P<post_id>\d+)$', 'socialnetwork.comments_views.add_comment',
                           name='add-comment'),
                       url(r'^login$', 'django.contrib.auth.views.login',
                           {'template_name': 'socialnetwork/login.html',
                            'authentication_form': LoginForm},
                           name='login'),
                       url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
                       ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
