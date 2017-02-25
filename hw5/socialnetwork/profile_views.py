import sys
import urllib
import buttons_views

from itertools import chain

from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from socialnetwork.models import *
from socialnetwork.forms import *


def is_following(profile, view_user):
   if(profile.followers.all().filter(user=view_user)):
      return True
   else:
      return False

@login_required 
@transaction.atomic
def view_profile_user(request, view_user):
   logged_in_profile = get_object_or_404(Profile, user=request.user)

   user = get_object_or_404(User, username=view_user)
   profile = get_object_or_404(Profile, user=user)

   is_owner = request.user.username == view_user

   followers = profile.followers.all()
   #print is_following(profile, request.user)

   context = {'profile' : profile, 
               'logged_in_profile' : logged_in_profile,
               'is_owner' : is_owner,
               'username' : view_user,
               'pic_followers' : followers,
               'is_following' : is_following(logged_in_profile, user),
               'form' : PostForm()}
   return render(request, 'socialnetwork/view-profile.html', context)

@login_required
@transaction.atomic
def edit_profile(request):
   profile = get_object_or_404(Profile, user=request.user)
   form = ProfileForm(instance=profile)
   
   return render(request, 'socialnetwork/edit-profile.html', 
      {'form' : form, 'profile' : profile})

@login_required
@transaction.atomic
def edit_profile_img(request):
   profile = get_object_or_404(Profile, user=request.user)
   form = ProfileForm(request.POST, request.FILES, instance=profile)

   #print("image url is: %s", profile.img.url)
   if (not form.is_valid()):
      #print("not valid")
      return render(request, 'socialnetwork/edit-profile.html', 
         {'form' : form, 'profile' : profile})
   #print("form was valid")
   #print("image url is: %s", profile.img.url)

   form.save()
   return redirect(reverse('view-profile-user', kwargs={'view_user' : request.user.username}))

@login_required
@transaction.atomic
def edit_profile_pw(request):
   profile = get_object_or_404(Profile, user=request.user)
   form = ProfileForm(request.POST, instance=profile, user=request.user)

   if (not form.is_valid()):
      return render(request, 'socialnetwork/edit-profile.html', 
         {'form' : form, 'profile' : profile})

   blog_user = request.user
   clean_password = form.cleaned_data['password1']
   blog_user.password = make_password(clean_password)
   blog_user.save()
            
   auth_user = authenticate(username=request.user,
                            password=clean_password)
   login(request, auth_user)

   return redirect(reverse('view-profile-user', kwargs={'view_user' : request.user.username}))

@login_required
@transaction.atomic
def edit_profile_info(request):
   profile = get_object_or_404(Profile, user=request.user)
   form = ProfileForm(request.POST, instance=request.user)
   blog_user = request.user

   if (not form.is_valid()):
      return render(request, 'socialnetwork/edit-profile.html', 
         {'form' : form, 'profile' : profile})

   profile.age = form.cleaned_data['age']
   profile.birthday = form.cleaned_data['birthday']
   profile.self_description = form.cleaned_data['self_description']
   blog_user.first_name = form.cleaned_data['first_name']
   blog_user.last_name = form.cleaned_data['last_name']
   profile.save()
   blog_user.save()

   return redirect(reverse('view-profile-user', kwargs={'view_user' : request.user.username}))
