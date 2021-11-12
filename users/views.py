from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages

from .models import *
from .forms import *

def homePage(req):
    return render(req, 'users/index.html')

def registrationPage(req):

    if req.method == 'POST':
        fName = req.POST.get('fName')
        lName = req.POST.get('lName')
        email = req.POST.get('email')
        username = req.POST.get('username')
        password1 = req.POST.get('password1')
        password2 = req.POST.get('password2')

        myUser = User.objects.create_user(username, email, password1)
        myUser.first_name = fName
        myUser.last_name = lName
        myUser.save()

        messages.success(req, 'Congratulations '+fName+' '+lName+', Your account has been successfully created.')

        return redirect('login')
    
    context = {}
    return render(req,'users/register.html',context)


def loginPage(req):

    if req.method == 'POST':
        username = req.POST.get('username')
        password1 = req.POST.get('password1')

    context = {}
    return render(req,'users/login.html',context)


def logoutPage(req):
    logout(req)
    return redirect('home')