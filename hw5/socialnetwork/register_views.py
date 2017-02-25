import sys
import urllib

from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.http import HttpResponse, Http404
from django.contrib.auth.tokens import default_token_generator

from socialnetwork.models import *
from socialnetwork.forms import *

@transaction.atomic
def register_user(request):
   context = {}

   if (request.method == 'GET'):
      context['form'] = RegistrationForm()
      return render(request, 'socialnetwork/registration.html', context)
   
   form = RegistrationForm(request.POST)
   context['form'] = form

   if (not form.is_valid()):
      return render(request, 'socialnetwork/registration.html', context)
   
   new_user = User.objects.create_user(
      username=form.cleaned_data['username'],
      password=form.cleaned_data['password1'])

   new_user.is_active = True
   new_user.save()

   token = default_token_generator.make_token(new_user)

   new_profile = Profile(user=new_user)
   new_profile.save()

   return redirect(reverse('home'))

@transaction.atomic
def confirm_registration(request, username, token):
   user = get_object_or_404(User, username=username)

   if not default_token_generator.check_token(user, token):
      raise Http404

   user.is_active = True
   user.save()
   return redirect(reverse('home'))
