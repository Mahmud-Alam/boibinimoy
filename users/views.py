from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils.safestring import mark_safe

from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from . tokens import generate_token

from django.forms import EmailField
from django.core.exceptions import ValidationError

from boibinimoy import settings
from .models import *
from .forms import *

def homePage(request):
    return render(request, 'users/index.html')

def isEmailAddressValid( email ):
    try:
        EmailField().clean(email)
        return True
    except ValidationError:
        return False

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

        if isEmailAddressValid(email) == False:
            messages.error(request, mark_safe('&bull; "'+email+'" is invalid email!<br/>&bull; Please try valid email.'))
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
        
        # In default, when we create user, it will be user.is_active = True. So, now we will make in False and after click the confirmation email link, the user should be activated.
        myUser.is_active = False
        myUser.save()

        # Email address confirmation email, and by this confirmation, user will active.
        current_site = get_current_site(request)
        subject = "Confirmation Email from Boi-Binimoy!"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myUser.email]

        email_dict = {'name':myUser.first_name,'domain':current_site,'uid':urlsafe_base64_encode(force_bytes(myUser.pk)),'token':generate_token.make_token(myUser),}
        message = render_to_string('users/email_confirmation.html',email_dict)

        emailObj = EmailMessage(subject,message,from_email,to_list)
        emailObj.fail_silently = True
        emailObj.send()
        
        context = {'myUser':myUser}
        return render(request,'users/email_sent.html',context)
    
    return render(request,'users/register.html')

def accountActivate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myUser = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myUser = None

    context = {'myUser':myUser}
    if myUser is not None and generate_token.check_token(myUser, token):
        myUser.is_active = True
        myUser.save()
        login(request, myUser)
        return render(request, 'users/activation_successful.html',context)
    else:
        return render(request, 'users/activation_failed.html',context)


def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        userList = User.objects.filter(username=username)

        user = authenticate(request, username=username, password=password1)

        if user is not None:
            login(request, user)
            full_name = user.first_name+' '+user.last_name
            messages.success(request, full_name+' Login successfully!')
            return redirect('home')
        elif not userList:
            messages.error(request, mark_safe('&bull; Username is incorrect. Please try again.'))
        elif userList[0].is_active == False:
            messages.error(request, mark_safe('&bull; Account is not activated yet!<br/>&bull; Please check your confirmation email for activating your account.'))
        else:
            messages.error(request, mark_safe('&bull; Password is incorrect. Please try again.'))

    context = {}
    return render(request,'users/login.html',context)


def logoutPage(request):
    full_name = request.user.first_name+' '+request.user.last_name
    logout(request)
    messages.success(request, full_name+' Logout successfully!')
    return redirect('home')