# -*- coding: utf-8 -*-
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
from django.db.models import Q
from django.db.models import Count
from django.conf import settings


import pprint
from datetime import date, timedelta, datetime

# Create your views here.

def index(request):
  shirts = Shirt.objects.annotate(like_count=Count('like'))\
                        .order_by('-like_count')

  return render(request, 'index.html', {
    'css_list': [
      'home.css',
    ], 'shirts' :shirts
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
    search_word = request.GET.get('search_word')
    if search_word == None:
      search_word = ""
      search = False
      # return render_to_response('catalog.html', {'all_shirts': all_shirts, 'search': False})
    else:
      words = search_word.split()
      shirts = Shirt.objects.all()
      for word in words:
        shirts = shirts.filter(Q(name__icontains=word) | Q(description__icontains=word))
      all_shirts = shirts
      search = True
      # return HttpResponse(shirts)
      # return render_to_response('catalog.html', {'all_shirts': shirts, 'search': True, 'search_word': search_word})


    # expose filter selected options to the page
    filters = {
      'shirt_type': request.GET.get('shirt_type'),
      'attribute': request.GET.get('attribute'),
      'sort': request.GET.get('sort'),
    }

    # Filter by type of shirt
    if filters['shirt_type'] == 'waiting':
      all_shirts = all_shirts.filter(is_on_shelf=False)
    elif filters['shirt_type'] == 'on_shelf':
      all_shirts = all_shirts.filter(is_on_shelf=True)

    # Set order prefix
    order_prefix = ""
    if filters['sort'] == 'ZtoA':
      order_prefix = "-"

    # Set sort by
    if filters['attribute'] == 'name':
      all_shirts = all_shirts.order_by(order_prefix + 'name')
    elif filters['attribute'] == 'likes':
      all_shirts = all_shirts.annotate(like_count=Count('like')).order_by(order_prefix + 'like_count')
    elif filters['attribute'] == 'comments':
      all_shirts = all_shirts.annotate(comments_count=Count('comment')).order_by(order_prefix + 'comments_count')
    elif filters['attribute'] == 'price':
      all_shirts = all_shirts.order_by(order_prefix + 'color_num')

    # Add current amount of shirt join
    all_shirts = all_shirts.annotate(current_amount=Count('join'))

    return render_to_response('catalog.html', {
      'all_shirts': all_shirts,
      'css_list': [
        'catalog.css',
        'bootstrap-select.min.css',
      ],
      'js_list': [
        'bootstrap-select.min.js',
      ],
      'search': search,
      'search_word': search_word,
      'filters': filters,
    })

def search(request, search_word):
  words = search_word.split()
  # for word in words:

  return HttpResponse(words[0])

@login_required
def join(request, shirt_id):
  if request.method == 'GET':
    # show the view
    shirt = Shirt.objects.get(pk=shirt_id)
    shirt.current_amount = Join.objects.filter(shirt_id=shirt_id).count()
    
    shirt.comment_list = Comment.objects.filter(shirt_id=shirt_id)
    shirt.size_of_comment = shirt.comment_list.count
    
    shirt.like_count = Like.objects.filter(shirt_id=shirt_id).count()


    d = (shirt.waiting_id.require_date-date.today()).days
    shirt.created = (shirt.waiting_id.require_date-shirt.created_at.date()).days
    shirt.left = shirt.created - d
    shirt.percent_left = d*100/shirt.created
    shirt.people_left = shirt.current_amount * 100 / shirt.waiting_id.require_amount

    return render(request, 'join.html', {'shirt':shirt})

  elif request.method == 'POST':
    # do something interesting here !

    # redirect to another view
    return HttpResponseRedirect(reverse('status'))

def comment(request,comment_shirt_id):
  if request.method == 'POST'  and request.POST.get('comment_text') != "":
    cmt = request.POST.get('comment_text')
    b = Comment(user_id=request.user,shirt_id=Shirt.objects.get(pk=comment_shirt_id),comment=cmt,time=date.today())
    b.save()
  return HttpResponseRedirect('/join/' + comment_shirt_id + '/')
  

def like(request,like_shirt_id):
  if request.method == 'GET' and Like.objects.filter(user_id=request.user).count()==0:
      b = Like(user_id=request.user,shirt_id=Shirt.objects.get(pk=like_shirt_id),time=date.today())
      b.save()
  elif request.method == 'GET' and Like.objects.filter(user_id=request.user).count()==1:
      b = Like.objects.get(shirt_id=like_shirt_id,user_id=request.user)
      b.delete()

  return HttpResponseRedirect('/join/' + like_shirt_id + '/')


def buy(request, shirt_id):
  return render_to_response('buy.html', {})

def status_waiting(request):
  return render_to_response('status_waiting.html', {})

def status_in_progress(request):
  return render_to_response('status_in-progress.html', {})

def status_purchase_history(request):
  return render_to_response('status_purchased.html', {})

def payment(request):
  return render_to_response('payment.html', {})

def cart(request):
  return HttpResponse('cart')

@login_required
def design(request):
  if request.method == 'GET':
    context = RequestContext(request)
    return render_to_response('design.html', {
      'css_list': [ 'design.css' ],
      'js_list': ['dropzone.js'],
    }, context)

  elif request.method == 'POST':
    # file info
    file = request.FILES['file']
    name = file.name
    extension = name.split('.')[-1]
    # user info
    user = User.objects.get(username=request.user)
    # create a new shirt
    shirt = Shirt.objects.create(
      name=request.POST['name'],
      description=request.POST['description'],
      file_url=extension,
      shirt_color=0,
      owner_id=user,
      is_on_shelf=False,
      color_num=request.POST['color_num'],
      created_at=datetime.now() )

    # writintg the uploaded file
    newFilePath = settings.SHIRTS + '/' + str(shirt.id) + '.' + extension
    with open(newFilePath, 'wb+') as destination:
      for chunk in file.chunks():
        destination.write(chunk)

    return HttpResponse('success')

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
