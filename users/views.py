from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages

from .models import *
from .forms import *

def homePage(request):
    return render(request, 'users/index.html')

def registrationPage(request):

    if request.method == 'POST':
        fName = request.POST.get('fName')
        lName = request.POST.get('lName')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        myUser = User.objects.create_user(username, email, password1)
        myUser.first_name = fName
        myUser.last_name = lName
        myUser.save()

        full_name = request.user.first_name+' '+request.user.last_name
        messages.success(request, 'Congratulations '+full_name+', Your account has been created successfully.')
        return redirect('login')
    
    context = {}
    return render(request,'users/register.html',context)


def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')

        user = authenticate(request, username=username, password=password1)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username or password is incorrect')

    context = {}
    return render(request,'users/login.html',context)


def logoutPage(request):
    full_name = request.user.first_name+' '+request.user.last_name
    logout(request)
    messages.success(request, full_name+' Logout successfully!')
    return redirect('home')