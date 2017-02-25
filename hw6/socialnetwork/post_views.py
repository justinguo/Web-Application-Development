import sys
import urllib
from itertools import chain
import buttons_views

from django.core import serializers
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from socialnetwork.models import *
from socialnetwork.forms import *


@login_required
@transaction.atomic
def makepost_page(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'socialnetwork/make-post.html',
                  {'form': PostForm(), 'profile': profile})


@login_required
@transaction.atomic
def make_a_post(request):
    profile = get_object_or_404(Profile, user=request.user)
    new_post = Post(profile=profile)
    form = PostForm(request.POST, request.FILES, instance=new_post)

    if (not form.is_valid()):
        return render(request, 'socialnetwork/make-post.html', {'form': form,
                                                                'profile': profile})

    form.save()
    return redirect(reverse('home'))


@login_required
@transaction.atomic
def update_posts(request, post_id):
    profile = get_object_or_404(Profile, user=request.user)
    followers = profile.followers.all()
    response = []
    posts = Post.objects.filter(id__gt=post_id).filter(profile__in=followers)
    new_posts = []

    for post in posts:
        new_posts.append((post,
                          buttons_views.was_commented(post, request.user)))

    context = {'posts': new_posts, 'form': CommentForm(),
               'profile': profile}
    return render(request, 'socialnetwork/update-posts.html', context)
