from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from web.forms import UserForm, UserProfileForm
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db import models
from web.models import *

# Create your views here.

def index(request):
  return render(request, 'index.html', {
    'css_list': [
      'css.css',
      'test.css',
    ],
    'js_list': [
      'test.js'
    ]
  })

def logout(request):
  auth_logout(request)
  return HttpResponse("You are logout")

def signup(request):

  context = RequestContext(request) # get last inputs

  registered = False

  if request.method == 'POST':
    # POST Method for save userdata to database
    user_form = UserForm(data = request.POST)
    profile_form = UserProfileForm(data = request.POST)

    if user_form.is_valid() and profile_form.is_valid():

      user = user_form.save()

      user.set_password(user.password)
      user.save()   # save user to database

      profile = profile_form.save(commit=False)
      profile.user = user

      profile.save()

      registered = True

      return HttpResponseRedirect(reverse('login'))

    else:
      print user_form.errors, profile_form.errors




  else:
    # Create User Form
    user_form = UserForm()
    profile_form = UserProfileForm()

    # Return to the same page
  return render_to_response(
      'signup.html',
      {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
      context)


def login(request):
  context = RequestContext(request)
  if request.user.is_authenticated():
    return HttpResponseRedirect(reverse('index'))

  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)

    if user:
      auth_login(request, user)
      return HttpResponse('Login Success');
    else:
      print "Invalid login details: {0}, {1}".format(username, password)
      return HttpResponse("Invalid login")
  else:
    return render_to_response('login.html', {}, context)



def catalog(request):
  if request.method == 'GET':
    # return a view
    all_shirts = Shirt.objects.all()
    return render_to_response('catalog.html', {'all_shirts': all_shirts})

def search(request, search_word):
  return HttpResponse(search_word)

@login_required
def join(request):
  if request.method == 'GET':
    # show the view
    return render_to_response('join.html', {})
  elif request.method == 'POST':
    # do something interesting here !

    # redirect to another view
    return HttpResponseRedirect(reverse('status'))


def buy(request):
  return HttpResponse('buy')

def status_waiting(request):
  return HttpResponse('status_waiting')

def status_in_progress(request):
  return HttpResponse('status_in_progress')

def status_purchase_history(request):
  return HttpResponse('status_purchase_history')

def payment(request):
  return HttpResponse('payment')

def cart(request):
  return HttpResponse('cart')

@login_required
def design(request):
  return HttpResponse('design')

@login_required
def profile(request):
  return HttpResponse('profile')

@login_required
def withdraw(request):
  return HttpResponse('withdraw')

def admin(request):
  return HttpResponse('admin')


def restricted(request):
  return HttpResponse("Since you're logged in, you can see this text!")
