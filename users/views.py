from django.shortcuts import render
from .models import *

def home(req):
    return render(req, 'users/home.html')