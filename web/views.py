from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

# Create your views here.

def index(request):
  return render(request, 'index.html', {
    'test': 'mama'
    })

def catalog(request):
  if request.method == 'GET':
    # return a view

    return HttpResponse('catalog' + request.method)

def join(request):
  if request.method == 'GET':
    # show the view
    return HttpResponse('join')
  elif request.method == 'POST':
    # do something interesting here !

    # redirect to another view
    return HttpResponseRedirect(reverse('status'))


def buy(request):
  return HttpResponse('buy')

def status_waiting(request):
  return HttpResponse('status_waiting')

def status_in_progress(requset):
  return HttpResponse('status_in_progress')

def status_purchase_history(request):
  return HttpResponse('status_purchase_history')

def payment(request):
  return HttpResponse('payment')

def cart(request):
  return HttpResponse('cart')

def design(request):
  return HttpResponse('design')

def profile(request):
  return HttpResponse('profile')

def withdraw(request):
  return HttpResponse('withdraw')

def admin(request):
  return HttpResponse('admin')
