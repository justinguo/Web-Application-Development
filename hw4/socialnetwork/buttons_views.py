import sys
import urllib

from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404

from socialnetwork.models import *
from socialnetwork.forms import *

def was_followed(profile, post_user):
   if(profile.followers.all().filter(user=post_user)):
      return True
   else:
      return False

def was_blocked(profile, blocked_user):
   if(profile.blocked_users.filter(user=blocked_user)):
      return True
   else:
      return False

@login_required
@transaction.atomic
def follow(request, username):
   get_user = get_object_or_404(User, username=username)
   user_profile = get_object_or_404(Profile, user=get_user)
   profile = get_object_or_404(Profile, user=request.user)
   profile.followers.add(user_profile)
   profile.save()

   return redirect(reverse('home-followers'))

@login_required
@transaction.atomic
def unfollow(request, username):
   get_user = get_object_or_404(User, username=username)
   get_profile = get_object_or_404(Profile, user=get_user)
   profile = get_object_or_404(Profile, user=request.user)
   profile.followers.remove(get_profile)
   profile.save() 

   return redirect(reverse('home-followers'))
   