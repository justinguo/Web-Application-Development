from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from socialnetwork.models import *
from socialnetwork.forms import *   


@login_required
def home(request):
    context = {}
    context['posts'] = Post.objects.all().order_by("-post_time")
    context['form'] = PostForm()
    return render(request, 'socialnetwork/index.html', context)

@login_required
def add_post(request):
    new_post = Post(author=request.user)
    form = PostForm(request.POST, instance=new_post)
    if not form.is_valid():
    	context = {"form": form}
    	return render(request, 'socialnetwork/index.html', context)
    new_post.save()

    return redirect(reverse('home'))

@login_required
def user_post(request, id):
    context = {}
    
    try:
        user = User.objects.get(id=id)
    except:
        return redirect(reverse('home'))

    context['posts'] = Post.objects.filter(author=user).order_by("-post_time")
    context['profile'] = user
    context['form'] = PostForm()
    return render(request, 'socialnetwork/profile.html', context)

@transaction.atomic
def register(request):
    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'socialnetwork/register.html', context)

    form = RegistrationForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=request.POST['username'],
    									first_name=request.POST['first_name'],
    									last_name=request.POST['last_name'],
                                        password=request.POST['password1'],
                                        )
    new_user.is_active = True
    new_user.save()

    # Logs in the new user and redirects to the blog
    new_user = authenticate(username=request.POST['username'],
                            password=request.POST['password1'])
    
    if (new_user.is_active):
    	login(request, new_user)
    	return redirect(reverse('home'))
