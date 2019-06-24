from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    if request.session['username'] is None:
        return HttpResponse('index')
    else:
        return HttpResponse('Welcome ' + request.session['username'] + '!')