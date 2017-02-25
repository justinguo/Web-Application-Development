import sys
import urllib
import buttons_views

from itertools import chain

from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from socialnetwork.models import *
from socialnetwork.forms import *

@login_required
@transaction.atomic
def home(request):
   profile = get_object_or_404(Profile, user=request.user)
   posts = Post.objects.all()
 
   context = {'posts' : posts, 'profile' : profile, 
      'form' : PostForm()}
 
   return render(request, 'socialnetwork/home.html', context) 

@login_required
@transaction.atomic
def home_followers(request):
   profile = get_object_or_404(Profile, user=request.user)
   your_followers = profile.followers.all()

   posts = [] 
   for follower in your_followers:
      posts = list(chain(posts, follower.post_profile.all()))

   following_posts = []
   for post in posts:
      following_posts.append(
         (post,
          buttons_views.was_followed(profile, post.profile.user)
         ))

   context = {'posts' : following_posts, 'form' : PostForm(),
      'profile' : profile}

   return render(request, 'socialnetwork/home-followers.html', context)
