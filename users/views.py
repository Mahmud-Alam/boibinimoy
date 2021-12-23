from decimal import Context
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe

from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text

from books.models import Book
from .tokens import generate_token
from datetime import datetime, timedelta, timezone

from django.forms import EmailField
from django.core.exceptions import ValidationError

from boibinimoy import settings
from .models import *
from .forms import *
from .decorators import *

@admin_only
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
            messages.error(request, mark_safe('&bull; "'+email+'" is invalid email!<br/>&bull; Please try a valid email.'))
            return redirect('register')

        # if User.objects.filter(email=email):
        #     messages.error(request, mark_safe('&bull; "'+email+'" email already register!'))
        #     return redirect('register')
        
        if password1 != password2:
            messages.error(request, mark_safe('&bull; Password did not match!<br/>&bull; Please try again.'))
            return redirect('register')
        
        if len(password1)<8:
            messages.error(request, mark_safe('&bull; Password length must be 8 charecter!<br/>&bull; Please try a new password.'))
            return redirect('register')
        
        if password1.isdigit():
            messages.error(request, mark_safe('&bull; Password should not be only numeric charecters!<br/>&bull; Please try a new password.'))
            return redirect('register')
        
        if password1.isalpha():
            messages.error(request, mark_safe('&bull; Password should not be only letters!<br/>&bull; Please try a new password.'))
            return redirect('register')
        
        myUser = User.objects.create_user(username, email, password1, first_name=fName, last_name=lName)
        # myUser.first_name = fName
        # myUser.last_name = lName
        
        # In default, when we create user, it will be user.is_active = True. So, now we will make in False and after click the confirmation email link, the user should be activated.
        myUser.is_active = False
        myUser.save()

        # MOVE THESE CODES TO THE signals.py FILE
        customer = Customer.objects.create(username=myUser, first_name=fName, last_name=lName,email=email)
        group = Group.objects.get(name='customer')
        myUser.groups.add(group)
        myUser.save()


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
            'text1':"We're excited to have you get started. First, you need to confirm your account. Just press the button below.",
            }
        # message = render_to_string('users/email_confirmation.html',email_dict)

        # msg_plain = loader.render_to_string('email-templates/order-confirmation.txt', context) # The plain text version of the email
        # msg_html = loader.render_to_string('email-templates/order-confirmation.html', context) # The html version of the email

        # emailObj = EmailMessage(subject,message,from_email,to_list)
        # emailObj.fail_silently = True
        # emailObj.send()

        message_txt = render_to_string('users/email_confirmation.txt',email_dict)
        message_html = render_to_string('users/email_confirmation.html',email_dict)
        send_mail(subject, message_txt, from_email, to_list, fail_silently=True, html_message=message_html)
        
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
def userProfile(request, username):
    main_user = User.objects.get(username=username)
    if request.user.username == username:
        customer = Customer.objects.get(username=request.user)
        flag=True
    else:
        customer = Customer.objects.get(username=main_user)
        flag=False
    
    books = customer.book_set.order_by('-created')
    
    context = {'customer':customer,'books':books,'flag':flag}
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
            full_name = request.user.first_name+' '+request.user.last_name
            messages.success(request, full_name+', profile updated successfully!')
            return redirect('user-profile', username = request.user)

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
        
        message_txt = render_to_string('users/email_confirmation.txt',email_dict)
        message_html = render_to_string('users/email_confirmation.html',email_dict)
        send_mail(subject, message_txt, from_email, to_list, fail_silently=True, html_message=message_html)

        # emailObj = EmailMessage(subject,message_txt,from_email,to_list,html_message=message_html)
        # emailObj.fail_silently = True
        # emailObj.send()
    
        
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
            messages.error(request, mark_safe('&bull; "'+email+'" is invalid email address!<br/>&bull; Please try a valid email address.'))
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
        # message = render_to_string('users/email_confirmation.html',email_dict)

        # emailObj = EmailMessage(subject,message,from_email,to_list)
        # emailObj.fail_silently = True
        # emailObj.send()

        message_txt = render_to_string('users/email_confirmation.txt',email_dict)
        message_html = render_to_string('users/email_confirmation.html',email_dict)
        send_mail(subject, message_txt, from_email, to_list, fail_silently=True, html_message=message_html)
        
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def changePassword(request):
    myUser = User.objects.get(username=request.user)
    if request.method == 'POST':
        oldpassword = request.POST.get('oldpassword')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        user = authenticate(request, username=request.user, password=oldpassword)

        if user is not None:
            if len(password1)<8:
                messages.error(request, mark_safe('&bull; Password length must be 8 charecter!<br/>&bull; Please try a new password.'))
                return redirect('change-password')
            if password1.isdigit():
                messages.error(request, mark_safe('&bull; Password should not be only numeric charecters!<br/>&bull; Please try a new password.'))
                return redirect('change-password')
            if password1.isalpha():
                messages.error(request, mark_safe('&bull; Password should not be only letters!<br/>&bull; Please try a new password.'))
                return redirect('change-password')
            if password1 != password2:
                messages.error(request, mark_safe('&bull; New Password did not match!<br/>&bull; Please try again.'))
                return redirect('change-password')
        else:
            messages.error(request, mark_safe('&bull; Old Password is incorrect. Please try again.'))
            return redirect('change-password')
        
        # myUser.set_password(make_password(password1))
        myUser.set_password(password1)
        myUser.save()

        # userLogin = authenticate(request, username=request.user, password=password1)
        login(request, myUser)
        messages.success(request,'Congratulations "'+user.username+'"! Your password changed successfully!')
        return redirect('user-profile', username = request.user)

    context = {}
    return render(request,'users/change_password.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def adminPanel(request, username):
    admin = User.objects.get(username=username)
    customer = Customer.objects.all()
    customer_count = customer.count()
    book = Book.objects.all()
    book_count = book.count()

    total_admin = User.objects.filter(groups__name='admin')
    admin_count = total_admin.count()
    total_manager = User.objects.filter(groups__name='manager')
    manager_count = total_manager.count()
    
    context = {'admin':admin,'customer':customer,'customer_count':customer_count,'book':book,'book_count':book_count,
                'total_admin':total_admin,'admin_count':admin_count,'total_manager':total_manager,'manager_count':manager_count}
    return render(request,'admin/admin_panel.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addManager(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        #allUsers = User.objects.all().values_list('username',flat=True)
        allUsers = [i.lower() for i in User.objects.all().values_list('username',flat=True)]

        #if User.objects.filter(username=username):
        if username.lower() in allUsers:
            messages.error(request, mark_safe('&bull; "'+username+'" username already exists!<br/>&bull; Please try another username.'))
            return redirect('add-manager')

        if len(username)>15:
            messages.error(request, mark_safe('&bull; Username must be within 15 character.'))
            return redirect('add-manager')
        
        if not username.isalnum():
            messages.error(request, mark_safe('&bull; Username must be Alpha-Numeric!<br/>&bull; Please try another username.'))
            return redirect('add-manager')
        
        if username.isdigit():
            messages.error(request, mark_safe("&bull; Username can't be only Numeric!<br/>&bull; Please try another username."))
            return redirect('add-manager')

        if isEmailAddressValid(email) == False:
            messages.error(request, mark_safe('&bull; "'+email+'" is invalid email!<br/>&bull; Please try a valid email.'))
            return redirect('add-manager')

        # if User.objects.filter(email=email):
        #     messages.error(request, mark_safe('&bull; "'+email+'" email already register!'))
        #     return redirect('add-manager')
        
        if password1 != password2:
            messages.error(request, mark_safe('&bull; Password did not match!<br/>&bull; Please try again.'))
            return redirect('add-manager')
        
        if len(password1)<8:
            messages.error(request, mark_safe('&bull; Password length must be 8 charecter!<br/>&bull; Please try a new password.'))
            return redirect('add-manager')
        
        if password1.isdigit():
            messages.error(request, mark_safe('&bull; Password should not be only numeric charecters!<br/>&bull; Please try a new password.'))
            return redirect('add-manager')
        
        if password1.isalpha():
            messages.error(request, mark_safe('&bull; Password should not be only letters!<br/>&bull; Please try a new password.'))
            return redirect('register')
        
        newManager = User.objects.create_user(username, email, password1)
        newManager.save()

        manager = Manager.objects.create(username=newManager, email=email)
        group = Group.objects.get(name='manager')
        newManager.groups.add(group)
        newManager.save()
        messages.success(request,'New Manager "'+username+'" Added Successfully!')
        return redirect('admin-panel', username = request.user)

    context = {}
    return render(request,'admin/add_manager.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def manageUsers(request):
    total_customer = Customer.objects.all()
    total_admin = User.objects.filter(groups__name='admin')
    total_manager = User.objects.filter(groups__name='manager')

    context = {'total_admin':total_admin,'total_manager':total_manager}
    return render(request,'admin/manage_users.html',context)



##################################
# Manager User


@login_required(login_url='login')
@allowed_users(allowed_roles=['manager'])
def managerProfile(request, username):
    manager = Manager.objects.get(username=request.user)
    
    context = {'manager':manager}
    return render(request,'manager/manager_profile.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['manager'])
def editManagerProfile(request):
    manager = Manager.objects.get(username=request.user)
    myUser = User.objects.get(username=request.user)

    form = ManagerForm(instance=manager)
    if request.method == 'POST':
        form = ManagerForm(request.POST, request.FILES, instance=manager)
        if form.is_valid():
            form.save()
            myUser.first_name = manager.first_name
            myUser.last_name = manager.last_name
            myUser.save()
            full_name = manager.first_name+' '+manager.last_name
            messages.success(request, full_name+' Profile updated successfully!')
            return redirect('manager-profile', username = request.user)

    context = {'manager':manager,'myUser':myUser,'form':form}
    return render(request,'manager/edit_manager_profile.html',context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['manager'])
def managerDashboard(request, username):
    manager = Manager.objects.get(username=request.user)
    # manager = User.objects.get(username=username)
    total_admin = User.objects.filter(groups__name='admin')
    total_manager = User.objects.filter(groups__name='manager')
    total_customer = Customer.objects.all()
    total_book = Book.objects.all()
    
    context = {'manager':manager,'total_admin':total_admin,'total_manager':total_manager,'total_customer':total_customer,'total_book':total_book}
    return render(request,'manager/manager_dashboard.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['manager'])
def manageCustomers(request):
    manager = Manager.objects.get(username=request.user)
    total_customer = Customer.objects.all()

    context = {'total_customer':total_customer,'manager':manager}
    return render(request,'manager/manage_customers.html',context)
