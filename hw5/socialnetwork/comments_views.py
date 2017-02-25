import json
import sys
import urllib
import home_views

from django.core import serializers
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import formats
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404

from socialnetwork.models import *
from socialnetwork.forms import *


@login_required
@transaction.atomic
def add_comment(request, post_id):
    comment_form = CommentForm(request.POST)
    post = Post.objects.get(id=post_id)
    profile = get_object_or_404(Profile, user=request.user)

    if (not comment_form.is_valid()):
        return get_comments(request, post_id)

    new_comment = comment_form.save(commit=False)
    new_comment.post = post
    new_comment.profile = profile
    new_comment.username = request.user.username
    new_comment.save()

    return get_comments(request, post_id)


@login_required
@transaction.atomic
def get_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    response = []
    for comment in Comment.objects.filter(post=post):
        response.append({
            'img': comment.profile.img.url,
            'comment': comment.comment,
            'created_at': formats.date_format(comment.created_at, "DATETIME_FORMAT")
        })
    return HttpResponse(json.dumps(response), content_type="application/json")
