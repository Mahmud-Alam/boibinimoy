from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils.safestring import mark_safe

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

        if User.objects.filter(username=username):
            messages.error(request, mark_safe('&bull; "'+username+'" username already exists!<br/>&bull; Please try another username.'))
            return redirect('register')

        if len(username)>15:
            messages.error(request, mark_safe('&bull; Username must be within 15 character.'))
            return redirect('register')
        
        if not username.isalnum():
            messages.error(request, mark_safe('&bull; Username must be Alpha-Numeric.'))
            return redirect('register')

        if User.objects.filter(email=email):
            messages.error(request, mark_safe('&bull; "'+email+'" email already register!'))
            return redirect('register')
        
        if password1 != password2:
            messages.error(request, mark_safe('&bull; Password did not match!<br/>&bull; Please try again.'))
            return redirect('register')
        
        if len(password1)<8:
            messages.error(request, mark_safe('&bull; Password length must be 8 charecter!<br/>&bull; Please try new password.'))
            return redirect('register')
        
        if password1.isdigit():
            messages.error(request, mark_safe('&bull; Password should not be only numeric charecters!<br/>&bull; Please try new password.'))
            return redirect('register')
        
        if password1.isalpha():
            messages.error(request, mark_safe('&bull; Password should not be only letters!<br/>&bull; Please try new password.'))
            return redirect('register')
        

        myUser = User.objects.create_user(username, email, password1)
        myUser.first_name = fName
        myUser.last_name = lName
        myUser.save()

        full_name = fName+' '+lName
        messages.success(request, mark_safe('&bull; Congratulations '+full_name+'. <br/>&bull; Your account has been created successfully.'))
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
            messages.error(request, mark_safe('&bull; username or password is incorrect'))

    context = {}
    return render(request,'users/login.html',context)


def logoutPage(request):
    full_name = request.user.first_name+' '+request.user.last_name
    logout(request)
    messages.success(request, full_name+' Logout successfully!')
    return redirect('home')