from django.shortcuts import render
from django.http import HttpResponse

def books(req):
    return HttpResponse('all books')