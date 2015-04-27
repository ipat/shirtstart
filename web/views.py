# -*- coding: utf-8 -*-
from __future__ import division
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
from django.db.models import Count, Sum
from django.conf import settings


import pprint
from datetime import date, timedelta, datetime

# variable costs
PRICE_PER_SHIRT = 120
PRICE_PER_COLOR = 10
# fix costs
PRICE_BASE_BLOCK = 0
PRICE_BASE_PER_COLOR = 400
# how many people they can expect to buy their shirts
LARGEST_CROWD = 500
# money per shirt that designer will get
MONEY_PER_SHIRT = 10


# Create your views here.

def index(request):
  shirts = Shirt.objects\
            .annotate(like_count=Count('like'))\
            .order_by('-like_count')[:4]

  shirts = shirts.annotate(current_amount=Sum('join__amount'))

  return render(request, 'index.html', {
    'shirts' :shirts,
    'css_list': [
      'home.css',
    ],
  })

def logout(request):
  auth_logout(request)
  return HttpResponseRedirect(reverse('index'))

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
      return HttpResponseRedirect('/')
    else:
      print "Invalid login details: {0}, {1}".format(username, password)
      return HttpResponseRedirect('/login')
  else:
    return render_to_response('login.html', {}, context)



def catalog(request):
  user = request.user
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
      'shirt_type': request.GET.get('shirt_type') if request.GET.has_key('shirt_type') else '',
      'attribute': request.GET.get('attribute') if request.GET.has_key('attribute') else '',
      'sort': request.GET.get('sort') if request.GET.has_key('sort') else '',
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
    elif filters['attribute'] == 'time':
      all_shirts = all_shirts.order_by(order_prefix + 'created_at')
    else:
      all_shirts = all_shirts.order_by('-created_at')

    # Add current amount of shirt join
    all_shirts = all_shirts.annotate(current_amount=Sum('join__amount'))

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
      'user' : user,
    })

def search(request, search_word):
  words = search_word.split()
  # for word in words:

  return HttpResponse(words[0])

@login_required
def join(request, shirt_id):
  user = request.user
  if request.method == 'GET':
    # show the view
    shirt = Shirt.objects.get(pk=shirt_id)
    shirt.current_amount = 0
    for inJoin in Join.objects.filter(shirt_id=shirt_id):
      shirt.current_amount += inJoin.amount

    shirt.comment_list = Comment.objects.filter(shirt_id=shirt_id)
    shirt.size_of_comment = shirt.comment_list.count

    shirt.like_count = Like.objects.filter(shirt_id=shirt_id).count()


    d = (shirt.waiting_id.require_date-date.today()).days
    shirt.created = (shirt.waiting_id.require_date-shirt.created_at.date()).days
    shirt.left = shirt.created - d
    shirt.percent_left = d*100/shirt.created
    shirt.people_left = shirt.current_amount * 100 / shirt.waiting_id.require_amount
    try:
      like = Like.objects.filter(shirt_id=shirt_id).filter(user_id=user.id)
    except Like.DoesNotExist:
      like = None

    if len(like) == 0:
      is_like = False
    else:
      is_like = True

    ratio = (shirt.current_amount/shirt.waiting_id.require_amount)
    ratio_date = 1-(shirt.left/shirt.created)
    print 'ratio' + str(ratio_date) + ' ' + str(shirt.waiting_id.require_amount)
    return render(request, 'join.html', {
      'shirt':shirt,
      'css_list': [
        'join.css'
      ],
      'is_like': is_like,
      'ratio' : ratio,
      'ratio_date' : ratio_date,
    })

  elif request.method == 'POST':
    # do something interesting here !

    # redirect to another view
    return HttpResponseRedirect(reverse('status'))

def comment_join(request,comment_shirt_id):
  if request.method == 'POST'  and request.POST.get('comment_text') != "":
    cmt = request.POST.get('comment_text')
    b = Comment(user_id=request.user,shirt_id=Shirt.objects.get(pk=comment_shirt_id),comment=cmt,time=date.today())
    b.save()
  return HttpResponseRedirect('/join/' + comment_shirt_id + '/')


def like_join(request,like_shirt_id):
  if request.method == 'GET' and Like.objects.filter(user_id=request.user ,shirt_id=like_shirt_id).count()==0:
      b = Like(user_id=request.user,shirt_id=Shirt.objects.get(pk=like_shirt_id),time=date.today())
      b.save()
  elif request.method == 'GET' and Like.objects.filter(user_id=request.user, shirt_id=like_shirt_id).count()==1:
      b = Like.objects.get(shirt_id=like_shirt_id,user_id=request.user)
      b.delete()

  return HttpResponseRedirect('/join/' + like_shirt_id + '/')

def comment_buy(request,comment_shirt_id):
  if request.method == 'POST'  and request.POST.get('comment_text') != "":
    cmt = request.POST.get('comment_text')
    b = Comment(user_id=request.user,shirt_id=Shirt.objects.get(pk=comment_shirt_id),comment=cmt,time=date.today())
    b.save()
  return HttpResponseRedirect('/buy/' + comment_shirt_id + '/')




def like_buy(request,like_shirt_id):
  if request.method == 'GET' and Like.objects.filter(user_id=request.user ,shirt_id=like_shirt_id).count()==0:
      b = Like(user_id=request.user,shirt_id=Shirt.objects.get(pk=like_shirt_id),time=date.today())
      b.save()
  elif request.method == 'GET' and Like.objects.filter(user_id=request.user,shirt_id=like_shirt_id).count()==1:
      b = Like.objects.get(shirt_id=like_shirt_id,user_id=request.user)
      b.delete()

  return HttpResponseRedirect('/buy/' + like_shirt_id + '/')

# def cart(request):

#   return HttpResponseRedirect('/cart/')

def add_to_cart(request,add_shirt_id):

  try:
    sa = request.POST.get('sAmount')
    if request.POST.get('sAmount') != '':
      s_amount = int(sa) + Shirt_in_cart.objects.get(user_id=request.user,shirt_id=add_shirt_id,shirt_size=1).amount
      Shirt_in_cart.objects.filter(user_id=request.user,shirt_id=add_shirt_id,shirt_size=1).update(amount=s_amount)
  except Shirt_in_cart.DoesNotExist:
    if request.POST.get('sAmount') != '':
      s = Shirt_in_cart(user_id=request.user,shirt_id=Shirt.objects.get(pk=add_shirt_id),shirt_size=1,amount=request.POST.get('sAmount'),time=date.today())
      s.save()
  try:
    sm = request.POST.get('mAmount')
    if request.POST.get('mAmount') != '':
      m_amount = int(sm) + Shirt_in_cart.objects.get(user_id=request.user,shirt_id=add_shirt_id,shirt_size=2).amount
      Shirt_in_cart.objects.filter(user_id=request.user,shirt_id=add_shirt_id,shirt_size=2).update(amount=m_amount)
  except Shirt_in_cart.DoesNotExist:
    if request.POST.get('mAmount') != '':
      m = Shirt_in_cart(user_id=request.user,shirt_id=Shirt.objects.get(pk=add_shirt_id),shirt_size=2,amount=request.POST.get('mAmount'),time=date.today())
      m.save()
  try:
    sl = request.POST.get('lAmount')
    if request.POST.get('lAmount') != '':
      l_amount = int(sl) + Shirt_in_cart.objects.get(user_id=request.user,shirt_id=add_shirt_id,shirt_size=3).amount
      Shirt_in_cart.objects.filter(user_id=request.user,shirt_id=add_shirt_id,shirt_size=3).update(amount=l_amount)
  except Shirt_in_cart.DoesNotExist:
    if request.POST.get('lAmount') != '':
      l = Shirt_in_cart(user_id=request.user,shirt_id=Shirt.objects.get(pk=add_shirt_id),shirt_size=3,amount=request.POST.get('lAmount'),time=date.today())
      l.save()
  try:
    sxl = request.POST.get('xlAmount')
    if request.POST.get('xlAmount') != '':
      xl_amount = int(sxl) + Shirt_in_cart.objects.get(user_id=request.user,shirt_id=add_shirt_id,shirt_size=4).amount
      Shirt_in_cart.objects.filter(user_id=request.user,shirt_id=add_shirt_id,shirt_size=4).update(amount=xl_amount)
  except Shirt_in_cart.DoesNotExist:
    if request.POST.get('xlAmount') != '':
      xl = Shirt_in_cart(user_id=request.user,shirt_id=Shirt.objects.get(pk=add_shirt_id),shirt_size=4,amount=request.POST.get('xlAmount'),time=date.today())
      xl.save()

  return HttpResponseRedirect('/cart/' + add_shirt_id + '/')




@login_required
def buy(request, shirt_id):
  user = request.user
  shirt = Shirt.objects.get(pk=shirt_id)
  shirt.comment_list = Comment.objects.filter(shirt_id=shirt_id)
  shirt.size_of_comment = shirt.comment_list.count
  shirt.like_count = Like.objects.filter(shirt_id=shirt_id).count()

  try:
    like = Like.objects.filter(shirt_id=shirt_id).filter(user_id=user.id)
  except Like.DoesNotExist:
    like = None

  if len(like) == 0:
    is_like = False
  else:
    is_like = True

  return render(request,'buy.html', {
    'shirt':shirt,
    'css_list': [
      'buy.css'
    ],
    'is_like': is_like,
  })

@login_required
def status_waiting(request):
  user = request.user
  join = Join.objects.filter(user_id=request.user)
  join.user = request.user
  join.count = join.count()
  join.today = date.today()
  join_len = len(join)
  shirt_inpro = {}
  shirt_purhis = {}
  shirt_info_inpro = []
  try:
    order = Order.objects.filter(user_id=user.id)
    for o in order:
      if o.status == 0:
        order_list = Order_list.objects.filter(order_id=o.id)
        for order_item in order_list:
          shirt_inpro[str(order_item.id)] = ['a']*9
          shirt_inpro[str(order_item.id)][0] = order_item.shirt_id.name
          shirt_inpro[str(order_item.id)][1] = '0'
          shirt_inpro[str(order_item.id)][2] = '0'
          shirt_inpro[str(order_item.id)][3] = '0'
          shirt_inpro[str(order_item.id)][4] = '0'
          shirt_inpro[str(order_item.id)][5] = order_item.shirt_id.owner_id.username
          shirt_inpro[str(order_item.id)][6] = order_item.shirt_id.description
          shirt_inpro[str(order_item.id)][8] = order_item.shirt_id
      elif o.status == 1:
        order_list = Order_list.objects.filter(order_id=o.id)
        for order_item in order_list:
          shirt_purhis[str(order_item.id)] = ['a']*9
          shirt_purhis[str(order_item.id)][0] = order_item.shirt_id.name
          shirt_purhis[str(order_item.id)][1] = '0'
          shirt_purhis[str(order_item.id)][2] = '0'
          shirt_purhis[str(order_item.id)][3] = '0'
          shirt_purhis[str(order_item.id)][4] = '0'
          shirt_purhis[str(order_item.id)][5] = order_item.shirt_id.owner_id.username
          shirt_purhis[str(order_item.id)][6] = order_item.shirt_id.description
          shirt_purhis[str(order_item.id)][8] = order_item.shirt_id


    for o in order:
      if o.status == 0:
        order_list = Order_list.objects.filter(order_id=o.id)
        for order_item in order_list:
          if order_item.shirt_size == '1':
            shirt_inpro[str(order_item.id)][1] = order_item.amount
          elif order_item.shirt_size == '2':
            shirt_inpro[str(order_item.id)][2] = order_item.amount
          elif order_item.shirt_size == '3':
            shirt_inpro[str(order_item.id)][3] = order_item.amount
          elif order_item.shirt_size == '4':
            shirt_inpro[str(order_item.id)][4] = order_item.amount
          shirt_inpro[str(order_item.id)][7] = str((order_item.price_each) * ((int(shirt_inpro[str(order_item.id)][4])) + (int(shirt_inpro[str(order_item.id)][3])) + (int(shirt_inpro[str(order_item.id)][2])) + (int(shirt_inpro[str(order_item.id)][1]))))
      elif o.status == 1:
        order_list = Order_list.objects.filter(order_id=o.id)
        for order_item in order_list:
          if order_item.shirt_size == '1':
            shirt_purhis[str(order_item.id)][1] = order_item.amount
          elif order_item.shirt_size == '2':
            shirt_purhis[str(order_item.id)][2] = order_item.amount
          elif order_item.shirt_size == '3':
            shirt_purhis[str(order_item.id)][3] = order_item.amount
          elif order_item.shirt_size == '4':
            shirt_purhis[str(order_item.id)][4] = order_item.amount
          shirt_purhis[str(order_item.id)][7] = str((order_item.shirt_id.shirt_color * 30 + 50) * ((int(shirt_purhis[str(order_item.id)][4])) + (int(shirt_purhis[str(order_item.id)][3])) + (int(shirt_purhis[str(order_item.id)][2])) + (int(shirt_purhis[str(order_item.id)][1]))))
  except Shirt_in_cart.DoesNotExist:
    shirt_ordered = None
  noti_inpro = len(shirt_inpro)
  noti_purhis = len(shirt_purhis)
  return render_to_response('status_waiting.html', {
      'join':join,
      'user' : user,
      'join_len' : join_len,
      'noti_inpro' : noti_inpro,
      'noti_purhis' : noti_purhis,
      'css_list': [
        'status-waiting.css',
      ],
    })

@login_required
def status_in_progress(request):
  user = request.user
  join = Join.objects.filter(user_id=request.user)
  join.user = request.user
  join.count = join.count()
  join.today = date.today()
  join_len = len(join)
  shirt_inpro = {}
  shirt_purhis = {}
  shirt_info_inpro = []
  try:
    order = Order.objects.filter(user_id=user.id)
    for o in order:
      if o.status == 0:
        order_list = Order_list.objects.filter(order_id=o.id)
        for order_item in order_list:
          shirt_inpro[str(order_item.id)] = ['a']*9
          shirt_inpro[str(order_item.id)][0] = order_item.shirt_id.name
          shirt_inpro[str(order_item.id)][1] = '0'
          shirt_inpro[str(order_item.id)][2] = '0'
          shirt_inpro[str(order_item.id)][3] = '0'
          shirt_inpro[str(order_item.id)][4] = '0'
          shirt_inpro[str(order_item.id)][5] = order_item.shirt_id.owner_id.username
          shirt_inpro[str(order_item.id)][6] = order_item.shirt_id.description
          shirt_inpro[str(order_item.id)][8] = order_item.shirt_id
      elif o.status == 1:
        order_list = Order_list.objects.filter(order_id=o.id)
        for order_item in order_list:
          shirt_purhis[str(order_item.id)] = ['a']*9
          shirt_purhis[str(order_item.id)][0] = order_item.shirt_id.name
          shirt_purhis[str(order_item.id)][1] = '0'
          shirt_purhis[str(order_item.id)][2] = '0'
          shirt_purhis[str(order_item.id)][3] = '0'
          shirt_purhis[str(order_item.id)][4] = '0'
          shirt_purhis[str(order_item.id)][5] = order_item.shirt_id.owner_id.username
          shirt_purhis[str(order_item.id)][6] = order_item.shirt_id.description
          shirt_purhis[str(order_item.id)][8] = order_item.shirt_id


    for o in order:
      if o.status == 0:
        order_list = Order_list.objects.filter(order_id=o.id)
        for order_item in order_list:
          if order_item.shirt_size == '1':
            shirt_inpro[str(order_item.id)][1] = order_item.amount
          elif order_item.shirt_size == '2':
            shirt_inpro[str(order_item.id)][2] = order_item.amount
          elif order_item.shirt_size == '3':
            shirt_inpro[str(order_item.id)][3] = order_item.amount
          elif order_item.shirt_size == '4':
            shirt_inpro[str(order_item.id)][4] = order_item.amount
          shirt_inpro[str(order_item.id)][7] = str((order_item.price_each) * ((int(shirt_inpro[str(order_item.id)][4])) + (int(shirt_inpro[str(order_item.id)][3])) + (int(shirt_inpro[str(order_item.id)][2])) + (int(shirt_inpro[str(order_item.id)][1]))))
      elif o.status == 1:
        order_list = Order_list.objects.filter(order_id=o.id)
        for order_item in order_list:
          if order_item.shirt_size == '1':
            shirt_purhis[str(order_item.id)][1] = order_item.amount
          elif order_item.shirt_size == '2':
            shirt_purhis[str(order_item.id)][2] = order_item.amount
          elif order_item.shirt_size == '3':
            shirt_purhis[str(order_item.id)][3] = order_item.amount
          elif order_item.shirt_size == '4':
            shirt_purhis[str(order_item.id)][4] = order_item.amount
          shirt_purhis[str(order_item.id)][7] = str((order_item.shirt_id.shirt_color * 30 + 50) * ((int(shirt_purhis[str(order_item.id)][4])) + (int(shirt_purhis[str(order_item.id)][3])) + (int(shirt_purhis[str(order_item.id)][2])) + (int(shirt_purhis[str(order_item.id)][1]))))
  except Shirt_in_cart.DoesNotExist:
    shirt_ordered = None
  # return HttpResponse(shirt_inpro['5'])
  total = 0
  noti_inpro = len(shirt_inpro)
  noti_purhis = len(shirt_purhis)
  for sh in shirt_inpro:
    shirt_info_inpro.append(shirt_inpro[sh])

  return render_to_response('status_in-progress.html', {
    'shirt_amount' : shirt_info_inpro,
    'user' : user,
    'total' : total,
    'noti_inpro' : noti_inpro,
    'noti_purhis' : noti_purhis,
    'css_list': [
      'status-in-progress.css',
    ],
    'join_len' : join_len,
  })

@login_required
def status_purchase_history(request):
  user = request.user
  join = Join.objects.filter(user_id=request.user)
  join.user = request.user
  join.count = join.count()
  join.today = date.today()
  join_len = len(join)
  shirt_inpro = {}
  shirt_purhis = {}
  shirt_info_inpro = []
  shirt_info_purhis = []
  try:
    order = Order.objects.filter(user_id=user.id)
    for o in order:
      if o.status == 0:
        order_list = Order_list.objects.filter(order_id=o.id)
        for order_item in order_list:
          shirt_inpro[str(order_item.id)] = ['a']*9
          shirt_inpro[str(order_item.id)][0] = order_item.shirt_id.name
          shirt_inpro[str(order_item.id)][1] = '0'
          shirt_inpro[str(order_item.id)][2] = '0'
          shirt_inpro[str(order_item.id)][3] = '0'
          shirt_inpro[str(order_item.id)][4] = '0'
          shirt_inpro[str(order_item.id)][5] = order_item.shirt_id.owner_id.username
          shirt_inpro[str(order_item.id)][6] = order_item.shirt_id.description
          shirt_inpro[str(order_item.id)][8] = order_item.shirt_id
      elif o.status == 1:
        order_list = Order_list.objects.filter(order_id=o.id)
        for order_item in order_list:
          shirt_purhis[str(order_item.id)] = ['a']*9
          shirt_purhis[str(order_item.id)][0] = order_item.shirt_id.name
          shirt_purhis[str(order_item.id)][1] = '0'
          shirt_purhis[str(order_item.id)][2] = '0'
          shirt_purhis[str(order_item.id)][3] = '0'
          shirt_purhis[str(order_item.id)][4] = '0'
          shirt_purhis[str(order_item.id)][5] = order_item.shirt_id.owner_id.username
          shirt_purhis[str(order_item.id)][6] = order_item.shirt_id.description
          shirt_purhis[str(order_item.id)][8] = order_item.shirt_id


    for o in order:
      if o.status == 0:
        order_list = Order_list.objects.filter(order_id=o.id)
        for order_item in order_list:
          if order_item.shirt_size == '1':
            shirt_inpro[str(order_item.id)][1] = order_item.amount
          elif order_item.shirt_size == '2':
            shirt_inpro[str(order_item.id)][2] = order_item.amount
          elif order_item.shirt_size == '3':
            shirt_inpro[str(order_item.id)][3] = order_item.amount
          elif order_item.shirt_size == '4':
            shirt_inpro[str(order_item.id)][4] = order_item.amount
          shirt_inpro[str(order_item.id)][7] = str((order_item.price_each) * ((int(shirt_inpro[str(order_item.id)][4])) + (int(shirt_inpro[str(order_item.id)][3])) + (int(shirt_inpro[str(order_item.id)][2])) + (int(shirt_inpro[str(order_item.id)][1]))))
      elif o.status == 1:
        order_list = Order_list.objects.filter(order_id=o.id)
        for order_item in order_list:
          if order_item.shirt_size == '1':
            shirt_purhis[str(order_item.id)][1] = order_item.amount
          elif order_item.shirt_size == '2':
            shirt_purhis[str(order_item.id)][2] = order_item.amount
          elif order_item.shirt_size == '3':
            shirt_purhis[str(order_item.id)][3] = order_item.amount
          elif order_item.shirt_size == '4':
            shirt_purhis[str(order_item.id)][4] = order_item.amount
          shirt_purhis[str(order_item.id)][7] = str((order_item.shirt_id.shirt_color * 30 + 50) * ((int(shirt_purhis[str(order_item.id)][4])) + (int(shirt_purhis[str(order_item.id)][3])) + (int(shirt_purhis[str(order_item.id)][2])) + (int(shirt_purhis[str(order_item.id)][1]))))
  except Shirt_in_cart.DoesNotExist:
    shirt_ordered = None
  # return HttpResponse(shirt_inpro['5'])
  total = 0
  noti_inpro = len(shirt_inpro)
  noti_purhis = len(shirt_purhis)
  for sh in shirt_inpro:
    shirt_info_inpro.append(shirt_inpro[sh])

  return render_to_response('status_purchased.html', {
    'shirt_amount' : shirt_info_purhis,
    'user' : user,
    'total' : total,
    'noti_inpro' : noti_inpro,
    'noti_purhis' : noti_purhis,
    'css_list': [
      'status-purchase-history.css',
    ],
    'join_len' : join_len,
  })

@login_required
def payment(request, shirt_id):
  if request.method == 'GET':
    shirt_amount = {
      1: request.GET.get('sAmount'),
      2: request.GET.get('mAmount'),
      3: request.GET.get('lAmount'),
      4: request.GET.get('xlAmount')
    }

    shirt = Shirt.objects.get(pk=shirt_id)

    user_profile = UserProfile.objects.get(user_id=request.user.id)
    try:
      credit = Credit_card.objects.get(user_id=request.user.id)
      credit.exp = credit.expiry_year + "-" + credit.expiry_month
    except Credit_card.DoesNotExist:
      credit = None


    # credit.exp = (credit.expiry_year, credit.expiry_month)

    shirt = Shirt.objects.get(pk=shirt_id)
    # return HttpResponse(user_profile.address_building)

    return render(request,'payment.html', {'shirt': shirt, 'shirt_amount': shirt_amount, 'credit': credit, 'user_profile': user_profile, 'shirt_amount': shirt_amount})

  else:

    shirt_amount = {
      1: request.POST.get('sAmount'),
      2: request.POST.get('mAmount'),
      3: request.POST.get('lAmount'),
      4: request.POST.get('xlAmount')
    }

    # return HttpResponse(shirt_amount[2])

    input_info = request.POST
    user_profile = UserProfile.objects.get(user_id=request.user.id)
    user_profile.address_house_no = input_info.get('address_house_no')
    user_profile.address_building = input_info.get('address_building')
    user_profile.address_road = input_info.get('address_road')
    user_profile.address_subdistrict = input_info.get('address_subdistrict')
    user_profile.address_district = input_info.get('address_district')
    user_profile.address_province = input_info.get('address_province')
    user_profile.address_country = input_info.get('address_country')
    user_profile.address_postcode = input_info.get('address_postcode')
    user_profile.save()

    try:
      credit = Credit_card.objects.get(user_id=request.user.id)
      credit.name_on_card = input_info.get('name_on_card')
      credit.number = input_info.get('number')
      credit.expiry_month = input_info.get('expiry_month').split('-')[1]
      credit.expiry_year = input_info.get('expiry_month').split('-')[0]
      credit.save()
    except Credit_card.DoesNotExist:
      credit = Credit_card.objects.create(user_id=User.objects.get(pk=request.user.id), name_on_card=input_info.get('name_on_card'), number=input_info.get('number'), expiry_month=input_info.get('expiry_month').split('-')[1], expiry_year=input_info.get('expiry_month').split('-')[0])
      # credit.save()


    for i in range(1,4):
      if shirt_amount[i] != "":
        join_shirt = Join.objects.create(
          address_house_no = input_info.get('address_house_no'),
          address_building = input_info.get('address_building'),
          address_road = input_info.get('address_road'),
          address_subdistrict = input_info.get('address_subdistrict'),
          address_district = input_info.get('address_district'),
          address_province = input_info.get('address_province'),
          address_country = input_info.get('address_country'),
          address_postcode = input_info.get('address_postcode'),
          shirt_size = i,
          amount = shirt_amount[i],
          time = datetime.now(),
          user_id = User.objects.get(pk=request.user.id),
          shirt_id = Shirt.objects.get(pk=shirt_id))

    # user_profile.save(request.POST)
    # credit = Credit_card.objects.get(user_id=request.user.id)
    # credit.save(request.POST)
    return HttpResponseRedirect('/status/waiting')

@login_required
def checkout(request):
  if request.method == 'GET':
    user_profile = UserProfile.objects.get(user_id=request.user.id)
    try:
      credit = Credit_card.objects.get(user_id=request.user.id)
      credit.exp = credit.expiry_year + "-" + credit.expiry_month
    except Credit_card.DoesNotExist:
      credit = None

    return render(request,'checkout.html', {'credit': credit, 'user_profile': user_profile})

  else:
    input_info = request.POST
    user_profile = UserProfile.objects.get(user_id=request.user.id)
    user_profile.address_house_no = input_info.get('address_house_no')
    user_profile.address_building = input_info.get('address_building')
    user_profile.address_road = input_info.get('address_road')
    user_profile.address_subdistrict = input_info.get('address_subdistrict')
    user_profile.address_district = input_info.get('address_district')
    user_profile.address_province = input_info.get('address_province')
    user_profile.address_country = input_info.get('address_country')
    user_profile.address_postcode = input_info.get('address_postcode')
    user_profile.save()

    try:
      credit = Credit_card.objects.get(user_id=request.user.id)
      credit.name_on_card = input_info.get('name_on_card')
      credit.number = input_info.get('number')
      credit.expiry_month = input_info.get('expiry_month').split('-')[1]
      credit.expiry_year = input_info.get('expiry_month').split('-')[0]
      credit.save()
    except Credit_card.DoesNotExist:
      credit = Credit_card.objects.create(user_id=User.objects.get(pk=request.user.id), name_on_card=input_info.get('name_on_card'), number=input_info.get('number'), expiry_month=input_info.get('expiry_month').split('-')[1], expiry_year=input_info.get('expiry_month').split('-')[0])


    order = Order.objects.create(
      time = datetime.now(),
      address_house_no = input_info.get('address_house_no'),
      address_building = input_info.get('address_building'),
      address_road = input_info.get('address_road'),
      address_subdistrict = input_info.get('address_subdistrict'),
      address_district = input_info.get('address_district'),
      address_province = input_info.get('address_province'),
      address_country = input_info.get('address_country'),
      address_postcode = input_info.get('address_postcode'),
      status = 0,
      user_id = User.objects.get(pk=request.user.id))

    order_lists = Shirt_in_cart.objects.filter(user_id=request.user.id)

    for od in order_lists:
      price_each = PRICE_PER_SHIRT + od.shirt_id.color_num * PRICE_PER_COLOR
      Order_list.objects.create(
        shirt_size = od.shirt_size,
        amount = od.amount,
        order_id = order,
        shirt_id = od.shirt_id,
        price_each = price_each,)
      print od.shirt_id.owner_id
      designer = Designer.objects.get(user_id=od.shirt_id.owner_id)
      designer.wallet = designer.wallet + MONEY_PER_SHIRT * od.amount
      designer.save()
      od.delete()

    return HttpResponseRedirect('/status/in-progress/')


@login_required
def cart(request):
  user = request.user
  shirt_amount = {}
  shirt_if = []
  try:
    shirt_in_cart = Shirt_in_cart.objects.filter(user_id=user.id)
    for shirt in shirt_in_cart:
      shirt_amount[str(shirt.shirt_id.id)] = ['a']*9
      shirt_amount[str(shirt.shirt_id.id)][0] = shirt.shirt_id.name
      shirt_amount[str(shirt.shirt_id.id)][1] = '0'
      shirt_amount[str(shirt.shirt_id.id)][2] = '0'
      shirt_amount[str(shirt.shirt_id.id)][3] = '0'
      shirt_amount[str(shirt.shirt_id.id)][4] = '0'
      shirt_amount[str(shirt.shirt_id.id)][5] = shirt.shirt_id.owner_id.username
      shirt_amount[str(shirt.shirt_id.id)][6] = shirt.shirt_id.description


    for shirt in shirt_in_cart:
      if shirt.shirt_size == '1':
        shirt_amount[str(shirt.shirt_id.id)][1] = shirt.amount
      elif shirt.shirt_size == '2':
        shirt_amount[str(shirt.shirt_id.id)][2] = shirt.amount
      elif shirt.shirt_size == '3':
        shirt_amount[str(shirt.shirt_id.id)][3] = shirt.amount
      elif shirt.shirt_size == '4':
        shirt_amount[str(shirt.shirt_id.id)][4] = shirt.amount
      shirt_amount[str(shirt.shirt_id.id)][7] = str((shirt.shirt_id.color_num * PRICE_PER_COLOR + PRICE_PER_SHIRT) * ((int(shirt_amount[str(shirt.shirt_id.id)][4])) + (int(shirt_amount[str(shirt.shirt_id.id)][3])) + (int(shirt_amount[str(shirt.shirt_id.id)][2])) + (int(shirt_amount[str(shirt.shirt_id.id)][1]))))
      shirt_amount[str(shirt.shirt_id.id)][8] = shirt.shirt_id.id
  except Shirt_in_cart.DoesNotExist:
    shirt_in_cart = None
  # return HttpResponse(shirt_amount['5'])
  total = 0

  for sh in shirt_amount:
    shirt_if.append(shirt_amount[sh])
    total += int(shirt_amount[sh][7])

  len_cart = len(shirt_if)

  return render_to_response('cart.html', {
    'shirt_amount' : shirt_if,
    'user' : user,
    'total' : total,
    'css_list': [
      'cart.css',
    ],
    'len' : len_cart,
  })

def delete_in_cart(request, shirt_id):
  if shirt_id == '0':
    Shirt_in_cart.objects.filter(user_id = request.user.id).delete()
  else :
    try:
        Shirt_in_cart.objects.get(user_id=request.user.id, shirt_id=shirt_id).delete()
    except Shirt_in_cart.DoesNotExist:
      user_profile = None
  return HttpResponseRedirect('/cart/')


@login_required
def design(request):
  if request.method == 'GET':
    context = RequestContext(request)
    return render_to_response('design.html', {
      'costs' : {
        'price_per_shirt': PRICE_PER_SHIRT,
        'price_per_color': PRICE_PER_COLOR,
        'price_base_block': PRICE_BASE_BLOCK,
        'price_base_per_color': PRICE_BASE_PER_COLOR,
        'test': {
          'eiei': 12,
        },
      },
      'css_list': [
        'design.css',
        'bootstrap-slider.min.css',
      ],
      'js_list': [
        'dropzone.js',
        'bootstrap-slider.min.js',
      ],
    }, context)

  elif request.method == 'POST':
    # file info
    file = request.FILES['file']
    name = file.name
    extension = name.split('.')[-1]
    # user info
    user = User.objects.get(username=request.user)
    # create a waiting shirt
    time_d = timedelta(days=int(request.POST['require_days']))
    require_date = datetime.now() + time_d
    waiting = Waiting.objects.create(
      require_amount=request.POST['require_amount'],
      require_date=require_date)
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

    user_profile = UserProfile.objects.get(user_id=user.id)
    user_profile.is_designer = True
    user_profile.save()

    try:
      Designer.objects.get(user_id=user.id)
    except Designer.DoesNotExist:
      designer = Designer.objects.create(
        wallet=0,
        user_id=user,
      )

    # writintg the uploaded file
    newFilePath = settings.SHIRTS + '/' + str(shirt.id) + '.' + extension
    with open(newFilePath, 'wb+') as destination:
      for chunk in file.chunks():
        destination.write(chunk)

    return HttpResponse('success')

@login_required
def profile(request):
  user = request.user
  try:
    user_profile = UserProfile.objects.get(user_id=user.id)
  except UserProfile.DoesNotExist:
      user_profile = None
  try:
    all_shirts = Shirt.objects.filter(owner_id=user.id)
  except Shirt.DoesNotExist:
      all_shirts = None
  try:
    credit = Credit_card.objects.get(user_id=user.id)
  except Credit_card.DoesNotExist:
      credit = None
  try:
    designer = Designer.objects.get(user_id=user.id)
  except Designer.DoesNotExist:
      designer = None

  address = str(user_profile.address_house_no)+ ' ' + str(user_profile.address_building)+ ' ' + str(user_profile.address_road)+ ' ' + str(user_profile.address_subdistrict)+ ' ' + str(user_profile.address_district)+ ' ' + str(user_profile.address_province)+ ' ' + str(user_profile.address_country)+ ' ' + str(user_profile.address_postcode)
  if address == '       ':
    address = "None"
  print 'ad' + address
  return render_to_response('profile.html', {
    'user' : user,
    'user_profile' : user_profile,
    'credit' : credit,
    'all_shirts' : all_shirts,
    'designer' : designer,
    'address' : address,
    })

@login_required
def withdraw(request):
  if request.method == 'GET':
    user = request.user
    try:
      designer = Designer.objects.get(user_id=user.id)
    except Designer.DoesNotExist:
        designer = None

    trans = Transaction.objects.filter(user_id=user.id)

    return render(request, 'withdraw.html', {
        'designer' : designer,
        'trans': trans,
      })
  else :
    designer = Designer.objects.get(user_id=request.user.id)
    if request.POST.get('amount') == '':
      return HttpResponseRedirect('/withdraw')
    if int(request.POST.get('amount')) > designer.wallet:
      return HttpResponseRedirect('/withdraw')

    designer.wallet = designer.wallet - int(request.POST.get('amount'))
    designer.bank_account_bank = request.POST.get('bank_account_bank')
    designer.bank_account_number = request.POST.get('bank_account_number')
    designer.bank_account_name = request.POST.get('bank_account_name')
    designer.save()

    transaction = Transaction.objects.create(
      user_id=User.objects.get(pk=request.user.id),
      to_account_bank=request.POST.get('bank_account_bank'),
      to_account_number=request.POST.get('bank_account_number'),
      to_account_name=request.POST.get('bank_account_name'),
      time=datetime.now(),
      amount=int(request.POST.get('amount')) )



    return HttpResponseRedirect('/withdraw')

def admin_login(request):
  if request.session.get('admin_login') == True:
    return HttpResponseRedirect('/admin/')
  if request.method == 'GET':
    return render(request, 'admin_login.html')
  else :
    username = request.POST.get('username')
    password = request.POST.get('password')

    if username == 'shirt' and password == 'start':
      request.session['admin_login'] = True
      return HttpResponseRedirect('/admin/')
    else:
      return HttpResponseRedirect('/admin_login/')


def admin(request):

  if request.session.get('admin_login') != True:
    return HttpResponseRedirect('/admin_login/')

  if request.method == 'GET':

    in_progress = Order.objects.filter(status=False)
    for ip in in_progress:
      ip.total_price = 0
      ip.order_list = Order_list.objects.filter(order_id=ip.id)
      for od in ip.order_list:
        ip.total_price += od.amount*od.price_each
        if od.shirt_size == '1':
          od.shirt_size = 'S'
        elif od.shirt_size == '2':
          od.shirt_size = 'M'
        elif od.shirt_size == '3':
          od.shirt_size = 'L'
        elif od.shirt_size == '4':
          od.shirt_size = 'XL'

    sent = Order.objects.filter(status=True)
    for se in sent:
      se.total_price = 0
      se.order_list = Order_list.objects.filter(order_id=se.id)
      for od in se.order_list:
        se.total_price += od.amount*od.price_each

    return render(request, 'admin.html', {
      'css_list': [
        'admin.css'
      ],
      'in_progress' : in_progress,
      'sent': sent,

    })
  else :

    ship_tracking_no = request.POST.get('ship_tracking_no')
    order_id = request.POST.get('order_id')

    order = Order.objects.get(pk=order_id)
    order.ship_date = datetime.now()
    order.status = True
    order.ship_tracking_no = ship_tracking_no
    order.save()

    return HttpResponseRedirect('/admin/')

def restricted(request):
  return HttpResponse("Since you're logged in, you can see this text!")

def admin_logout(request):
  request.session['admin_login'] = False
  return HttpResponseRedirect('/admin/')