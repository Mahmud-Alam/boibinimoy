from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe

from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from .tokens import generate_token

from django.forms import EmailField
from django.core.exceptions import ValidationError

from boibinimoy import settings
from .models import *
from .forms import *
from .decorators import *

def homePage(request):
    return render(request, 'users/index.html')

def isEmailAddressValid( email ):
    try:
        EmailField().clean(email)
        return True
    except ValidationError:
        return False

@unauthenticated_user
def registrationPage(request):
    if request.method == 'POST':
        fName = request.POST.get('fName')
        lName = request.POST.get('lName')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        #allUsers = User.objects.all().values_list('username',flat=True)
        allUsers = [i.lower() for i in User.objects.all().values_list('username',flat=True)]

        #if User.objects.filter(username=username):
        if username.lower() in allUsers:
            messages.error(request, mark_safe('&bull; "'+username+'" username already exists!<br/>&bull; Please try another username.'))
            return redirect('register')

        if len(username)>15:
            messages.error(request, mark_safe('&bull; Username must be within 15 character.'))
            return redirect('register')
        
        if not username.isalnum():
            messages.error(request, mark_safe('&bull; Username must be Alpha-Numeric!<br/>&bull; Please try another username.'))
            return redirect('register')
        
        if username.isdigit():
            messages.error(request, mark_safe("&bull; Username can't be only Numeric!<br/>&bull; Please try another username."))
            return redirect('register')

        if isEmailAddressValid(email) == False:
            messages.error(request, mark_safe('&bull; "'+email+'" is invalid email!<br/>&bull; Please try valid email.'))
            return redirect('register')

        # if User.objects.filter(email=email):
        #     messages.error(request, mark_safe('&bull; "'+email+'" email already register!'))
        #     return redirect('register')
        
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
        
        myUser = User.objects.create_user(username, email, password1, first_name=fName, last_name=lName)
        # myUser.first_name = fName
        # myUser.last_name = lName
        
        # In default, when we create user, it will be user.is_active = True. So, now we will make in False and after click the confirmation email link, the user should be activated.
        myUser.is_active = False
        myUser.save()

        # MOVE THESE CODES TO THE signals.py FILE
        # customer = Customer.objects.create(username=myUser, first_name=fName, last_name=lName,email=email)
        # group = Group.objects.get(name='customer')
        # myUser.groups.add(group)
        

        # Email address confirmation email, and by this confirmation, user will active.
        current_site = get_current_site(request)
        subject = "Confirmation Email from Boi-Binimoy!"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myUser.email]

        email_dict = {
            'name':myUser.first_name,
            'domain':current_site,
            'uid':urlsafe_base64_encode(force_bytes(myUser.pk)),
            'token':generate_token.make_token(myUser),
            'link':'account-activate',
            'text1':'Please confirm your email by clicking on the following link.',
            }
        message = render_to_string('users/email_confirmation.html',email_dict)

        emailObj = EmailMessage(subject,message,from_email,to_list)
        emailObj.fail_silently = True
        emailObj.send()
        
        context = {'myUser':myUser,'title':'Confirmation Email Sent!','text1':'confirmation email sent','text2':'activating your account'}
        return render(request,'users/email_sent.html',context)
    
    return render(request,'users/register.html')

def accountActivate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myUser = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myUser = None

    context = {
        'myUser':myUser,
        'successTitle':'Account Activated Successfully!',
        'successText1':'Your account has been activated successfully!',
        'failedTitle':'Account Activation Failed!',
        'failedText1':'your account activation is failed.',
        }
    if myUser is not None and generate_token.check_token(myUser, token):
        myUser.is_active = True
        myUser.save()
        login(request, myUser)
        return render(request, 'users/activation_successful.html',context)
    else:
        return render(request, 'users/activation_failed.html',context)

@unauthenticated_user
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userProfile(request):
    customer = Customer.objects.get(username=request.user)
    context = {'customer':customer}
    return render(request,'users/user_profile.html',context)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def editUserProfile(request):
    customer = Customer.objects.get(username=request.user)
    myUser = User.objects.get(username=request.user)

    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            myUser.first_name = customer.first_name
            myUser.last_name = customer.last_name
            myUser.save()
            return redirect('user-profile')

    context = {'myUser':request.user,'form':form}
    return render(request,'users/edit_user_profile.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def changeUsername(request):
    myUser = User.objects.get(username=request.user)
    if request.method == 'POST':
        username = request.POST.get('username')

        allUsers = [i.lower() for i in User.objects.all().values_list('username',flat=True)]

        #if User.objects.filter(username=username):
        if username.lower() == myUser.username.lower():
            messages.error(request, mark_safe('&bull; "'+username+'" is your current username!<br/>&bull; Please try another username.'))
            return redirect('change-username')
        
        if username.lower() in allUsers:
            messages.error(request, mark_safe('&bull; "'+username+'" username already exists!<br/>&bull; Please try another username.'))
            return redirect('change-username')

        if len(username)>15:
            messages.error(request, mark_safe('&bull; Username must be within 15 character.'))
            return redirect('change-username')
        
        if not username.isalnum():
            messages.error(request, mark_safe('&bull; Username must be Alpha-Numeric!<br/>&bull; Please try another username.'))
            return redirect('change-username')
        
        if username.isdigit():
            messages.error(request, mark_safe("&bull; Username can't be only Numeric!<br/>&bull; Please try another username."))
            return redirect('change-username')


        current_site = get_current_site(request)
        subject = "Change Username Request!"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myUser.email]

        email_dict = {
            'name':myUser.first_name,
            'username':username,
            'domain':current_site,
            'uid':urlsafe_base64_encode(force_bytes(myUser.pk)),
            'token':generate_token.make_token(myUser),
            'link':'change-username-confirm',
            'text1':'Change username request has been placed. Please click on the following link for changing your username.',
            }
        message = render_to_string('users/email_confirmation.html',email_dict)

        emailObj = EmailMessage(subject,message,from_email,to_list)
        emailObj.fail_silently = True
        emailObj.send()
        
        context = {'myUser':myUser,'title':'Change Username Request Sent!','text1':'change username request sent','text2':'changing your username'}
        return render(request,'users/email_sent.html',context)

    return render(request,'users/change_username.html')

def changeUsernameConfirm(request, uidb64, token, username):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myUser = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myUser = None

    context = {
        'myUser':myUser,
        'successTitle':'Changed Username Successfully!',
        'successText1':'Your username has been changed successfully!',
        'failedTitle':'Username Change Request Failed!',
        'failedText1':'your username change request is failed.',
        }
    if myUser is not None and generate_token.check_token(myUser, token):
        myUser.username = username
        myUser.save()
        return render(request, 'users/activation_successful.html',context)
    else:
        return render(request, 'users/activation_failed.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def changeEmail(request):
    myUser = User.objects.get(username=request.user)
    if request.method == 'POST':
        email = request.POST.get('email')

        if isEmailAddressValid(email) == False:
            messages.error(request, mark_safe('&bull; "'+email+'" is invalid email address!<br/>&bull; Please try valid email address.'))
            return redirect('register')

        # if User.objects.filter(email=email):
        #     messages.error(request, mark_safe('&bull; "'+email+'" email already register!'))
        #     return redirect('register')


        current_site = get_current_site(request)
        subject = "Change Email Address Request!"
        from_email = settings.EMAIL_HOST_USER
        to_list = [email]

        email_dict = {
            'name':myUser.first_name,
            'email':email,
            'domain':current_site,
            'uid':urlsafe_base64_encode(force_bytes(myUser.pk)),
            'token':generate_token.make_token(myUser),
            'link':'change-email-confirm',
            'text1':'Change email address request has been placed. Please click on the following link for changing your email address.',
            }
        message = render_to_string('users/email_confirmation.html',email_dict)

        emailObj = EmailMessage(subject,message,from_email,to_list)
        emailObj.fail_silently = True
        emailObj.send()
        
        context = {'myUser':myUser,'title':'Change Email Address Request Sent!','text1':'change email address request sent','text2':'changing your email address'}
        return render(request,'users/email_sent.html',context)

    return render(request,'users/change_email.html')

def changeEmailConfirm(request, uidb64, token, email):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myUser = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myUser = None

    context = {
        'myUser':myUser,
        'successTitle':'Changed Email Address Successfully!',
        'successText1':'Your email address has been changed successfully!',
        'failedTitle':'Email Address Change Request Failed!',
        'failedText1':'your email address change request is failed.',
        }
    if myUser is not None and generate_token.check_token(myUser, token):
        myUser.email = email
        myUser.save()

        customer = Customer.objects.get(username=myUser)
        customer.email = myUser.email
        customer.save()
        return render(request, 'users/activation_successful.html',context)
    else:
        return render(request, 'users/activation_failed.html',context)