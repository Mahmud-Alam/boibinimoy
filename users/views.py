from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.contrib import messages

from .models import *
from .forms import *

def homePage(req):
    return render(req, 'users/index.html')

def registrationPage(req):
    form = CreateUserForm()
    if req.method == 'Post':
        form = CreateUserForm(req.Post)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(req, 'Account was created for '+user)
            return redirect('home')
    
    context = {'form':form}
    return render(req,'users/register.html',context)


def loginPage(req):
    context = {}
    return render(req,'users/login.html',context)


def logoutPage(req):
    logout(req)
    return redirect('home')