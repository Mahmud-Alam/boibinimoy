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
from django.utils.text import slugify

from .tokens import generate_token
from datetime import datetime, timedelta, timezone

from django.forms import EmailField
from django.core.exceptions import ValidationError

from boibinimoy import settings
from .models import *
from .forms import *
from .decorators import *

from books.models import *
from books.forms import *

@visitors_only
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
@allowed_users(allowed_roles=['customer','manager'])
def userProfile(request, username):
    main_user = User.objects.get(username=username)
    customer = manager = 0
    if request.user.groups.all()[0].name == 'manager':
        manager  = Manager.objects.get(username=request.user)
    elif request.user.groups.all()[0].name == 'customer':
        customer = Customer.objects.get(username=request.user)
        
    if request.user.username == username:
        customerInfo = Customer.objects.get(username=request.user)
        flag=True
    else:
        customerInfo = Customer.objects.get(username=main_user)
        flag=False
    
    books = customerInfo.book_set.order_by('-created')
    
    context = {'customer':customer,'manager':manager,'customerInfo':customerInfo,'books':books,'flag':flag}
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

    context = {'myUser':request.user,'form':form,'customer':customer}
    return render(request,'users/edit_user_profile.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def changeUsername(request):
    myUser = User.objects.get(username=request.user)
    customer = Customer.objects.get(username=request.user)
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

    return render(request,'users/change_username.html',{'customer':customer})

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
    customer = Customer.objects.get(username=request.user)
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

    return render(request,'users/change_email.html',{'customer':customer})

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
    customer = Customer.objects.get(username=request.user)
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

    context = {'customer':customer}
    return render(request,'users/change_password.html',context)




##################################
# Admin User


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def adminProfile(request, username):
    admin = Admin.objects.get(username=request.user)
    
    context = {'admin':admin,'flag':True}
    return render(request,'admin/admin_profile.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def editAdminProfile(request):
    admin = Admin.objects.get(username=request.user)
    myUser = User.objects.get(username=request.user)

    form = AdminForm(instance=admin)
    if request.method == 'POST':
        form = AdminForm(request.POST, request.FILES, instance=admin)
        if form.is_valid():
            form.save()
            myUser.first_name = admin.first_name
            myUser.last_name = admin.last_name
            myUser.save()
            full_name = admin.first_name+' '+admin.last_name
            messages.success(request, full_name+' Profile updated successfully!')
            return redirect('admin-profile', username = request.user)

    context = {'admin':admin,'myUser':myUser,'form':form,'flag':True}
    return render(request,'admin/edit_admin_profile.html',context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def adminPanel(request, username):
    adminModelList = [i.username.username for i in Admin.objects.all()]
    user = User.objects.get(username=request.user)
    if user.username in adminModelList:
        flag = True
        admin = Admin.objects.get(username=request.user)
    else:
        flag = False
        admin = user
    customer = Customer.objects.all()
    customer_count = customer.count()
    book = Book.objects.all()
    book_count = book.count()

    total_admin = User.objects.filter(groups__name='admin')
    admin_count = total_admin.count()
    total_manager = User.objects.filter(groups__name='manager')
    manager_count = total_manager.count()
    
    context = {'admin':admin,'flag':flag,'customer':customer,'customer_count':customer_count,'book':book,'book_count':book_count,
                'total_admin':total_admin,'admin_count':admin_count,'total_manager':total_manager,'manager_count':manager_count}
    return render(request,'admin/admin_panel.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createAdmin(request):
    adminModelList = [i.username.username for i in Admin.objects.all()]
    user = User.objects.get(username=request.user)
    if user.username in adminModelList:
        flag = True
        admin = Admin.objects.get(username=request.user)
    else:
        flag = False
        admin = user

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
            return redirect('create-admin')

        if len(username)>15:
            messages.error(request, mark_safe('&bull; Username must be within 15 character.'))
            return redirect('create-admin')
        
        if not username.isalnum():
            messages.error(request, mark_safe('&bull; Username must be Alpha-Numeric!<br/>&bull; Please try another username.'))
            return redirect('create-admin')
        
        if username.isdigit():
            messages.error(request, mark_safe("&bull; Username can't be only Numeric!<br/>&bull; Please try another username."))
            return redirect('create-admin')

        if isEmailAddressValid(email) == False:
            messages.error(request, mark_safe('&bull; "'+email+'" is invalid email!<br/>&bull; Please try a valid email.'))
            return redirect('create-admin')

        # if User.objects.filter(email=email):
        #     messages.error(request, mark_safe('&bull; "'+email+'" email already register!'))
        #     return redirect('create-admin')
        
        if password1 != password2:
            messages.error(request, mark_safe('&bull; Password did not match!<br/>&bull; Please try again.'))
            return redirect('create-admin')
        
        if len(password1)<8:
            messages.error(request, mark_safe('&bull; Password length must be 8 charecter!<br/>&bull; Please try a new password.'))
            return redirect('create-admin')
        
        if password1.isdigit():
            messages.error(request, mark_safe('&bull; Password should not be only numeric charecters!<br/>&bull; Please try a new password.'))
            return redirect('create-admin')
        
        if password1.isalpha():
            messages.error(request, mark_safe('&bull; Password should not be only letters!<br/>&bull; Please try a new password.'))
            return redirect('create-admin')
        
        newAdmin = User.objects.create_user(username, email, password1)
        newAdmin.save()

        admin = Admin.objects.create(username=newAdmin, email=email)
        group = Group.objects.get(name='admin')
        newAdmin.groups.add(group)
        newAdmin.save()
        messages.success(request,'New Admin "'+username+'" Added Successfully!')
        return redirect('admin-panel', username = request.user)

    context = {'admin':admin,'flag':flag}
    return render(request,'admin/create_admin.html',context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createManager(request):
    adminModelList = [i.username.username for i in Admin.objects.all()]
    user = User.objects.get(username=request.user)
    if user.username in adminModelList:
        flag = True
        admin = Admin.objects.get(username=request.user)
    else:
        flag = False
        admin = user

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
            return redirect('create-manager')

        if len(username)>15:
            messages.error(request, mark_safe('&bull; Username must be within 15 character.'))
            return redirect('create-manager')
        
        if not username.isalnum():
            messages.error(request, mark_safe('&bull; Username must be Alpha-Numeric!<br/>&bull; Please try another username.'))
            return redirect('create-manager')
        
        if username.isdigit():
            messages.error(request, mark_safe("&bull; Username can't be only Numeric!<br/>&bull; Please try another username."))
            return redirect('create-manager')

        if isEmailAddressValid(email) == False:
            messages.error(request, mark_safe('&bull; "'+email+'" is invalid email!<br/>&bull; Please try a valid email.'))
            return redirect('create-manager')

        # if User.objects.filter(email=email):
        #     messages.error(request, mark_safe('&bull; "'+email+'" email already register!'))
        #     return redirect('create-manager')
        
        if password1 != password2:
            messages.error(request, mark_safe('&bull; Password did not match!<br/>&bull; Please try again.'))
            return redirect('create-manager')
        
        if len(password1)<8:
            messages.error(request, mark_safe('&bull; Password length must be 8 charecter!<br/>&bull; Please try a new password.'))
            return redirect('create-manager')
        
        if password1.isdigit():
            messages.error(request, mark_safe('&bull; Password should not be only numeric charecters!<br/>&bull; Please try a new password.'))
            return redirect('create-manager')
        
        if password1.isalpha():
            messages.error(request, mark_safe('&bull; Password should not be only letters!<br/>&bull; Please try a new password.'))
            return redirect('create-manager')
        
        newManager = User.objects.create_user(username, email, password1)
        newManager.save()

        manager = Manager.objects.create(username=newManager, email=email)
        group = Group.objects.get(name='manager')
        newManager.groups.add(group)
        newManager.save()
        messages.success(request,'New Manager "'+username+'" Added Successfully!')
        return redirect('admin-panel', username = request.user)

    context = {'admin':admin,'flag':flag}
    return render(request,'admin/create_manager.html',context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','manager'])
def manageAdministrators(request):
    total_admin = User.objects.filter(groups__name='admin')
    total_manager = User.objects.filter(groups__name='manager')
    user = User.objects.get(username=request.user)
    user_group = user.groups.all()[0].name

    if user_group == 'admin':
        adminModelList = [i.username.username for i in Admin.objects.all()]
        if user.username in adminModelList:
            flag = True
            admin = Admin.objects.get(username=request.user)
        else:
            flag = False
            admin = user
        context = {'total_admin':total_admin,'total_manager':total_manager,'admin':admin,'flag':flag}
        return render(request,'admin/admin_manage_administrators.html',context)
    elif user_group == 'manager':
        manager = Manager.objects.get(username=request.user)
        context = {'total_admin':total_admin,'total_manager':total_manager,'manager':manager}
        return render(request,'manager/manager_manage_administrators.html',context)




##################################
# Manager User
##################################


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
    total_admin = User.objects.filter(groups__name='admin')
    total_manager = User.objects.filter(groups__name='manager')
    total_customer = Customer.objects.all()
    total_book = Book.objects.all()

    total_category = Category.objects.order_by('name')
    cat_book_count = [Book.objects.filter(category=cat).count() for cat in total_category]
    latest_books = Book.objects.order_by('-created')[:5]

    # Zip sorted
    # sorted(zipped, key = lambda t: t[1])
    category_dict =  zip(total_category,cat_book_count)
    category_dict = sorted(category_dict, key = lambda t: t[1], reverse=True)
    
    context = {'manager':manager,'total_admin':total_admin,'total_manager':total_manager,'total_customer':total_customer,
                'total_book':total_book,'total_category':total_category,'category_dict':category_dict,'latest_books':latest_books}
    return render(request,'manager/manager_dashboard.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['manager'])
def manageCustomers(request):
    manager = Manager.objects.get(username=request.user)
    total_customer = Customer.objects.all()

    customer_book_count = [cus.book_set.all().count() for cus in total_customer]
    customer_dict = zip(total_customer,customer_book_count)
    customer_dict = sorted(customer_dict, key = lambda t: t[1], reverse=True)

    context = {'total_customer':total_customer,'manager':manager,'customer_dict':customer_dict}
    return render(request,'manager/manage_customers.html',context)


def deleteUser(request, username):
    myUser = User.objects.get(username=username)
    group = myUser.groups.all()[0].name

    if request.method == 'POST':
        myUser.is_active = False
        myUser.save()
        
        if group == 'customer':
            messages.success(request, '"'+username+'" '+group+' is deleted successfully!')
            return redirect('manage-customers')
        else:
            messages.success(request, '"'+username+'" '+group+' is deleted successfully!')
            return redirect('manage-administrators')

    context = {'object':myUser}
    return render(request,"temp/delete_object.html",context)


def reactiveUser(request, username):
    myUser = User.objects.get(username=username)
    group = myUser.groups.all()[0].name

    if request.method == 'POST':
        myUser.is_active = True
        myUser.save()
        
        if group == 'customer':
            messages.success(request, '"'+username+'" '+group+' is reactivated successfully!')
            return redirect('manage-customers')
        else:
            messages.success(request, '"'+username+'" '+group+' is reactivated successfully!')
            return redirect('manage-administrators')

    context = {'myUser':myUser}
    return render(request,"temp/reactive_object.html",context)


def bookList(request):
    manager = Manager.objects.get(username=request.user)
    book_list = Book.objects.order_by('-created')

    context = {'manager':manager,'book_list':book_list}
    return render(request, "manager/book_list.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['manager'])
def categoryList(request):
    manager = Manager.objects.get(username=request.user)
    total_category = Category.objects.order_by('name')
    cat_book_count = [Book.objects.filter(category=cat).count() for cat in total_category]

    # Zip sorted
    # sorted(zipped, key = lambda t: t[1])
    category_dict =  zip(total_category,cat_book_count)
    category_dict = sorted(category_dict, key = lambda t: t[1], reverse=True)


    context = {'total_category':total_category,'category_dict':category_dict,'manager':manager}
    return render(request, "manager/category_list.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['manager'])
def createCategory(request):
    manager = Manager.objects.get(username=request.user)
    task = "Create"

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        allCategories = [i.lower() for i in Category.objects.all().values_list('name',flat=True)]

        if name.lower() in allCategories:
            messages.error(request, mark_safe('&bull; "'+name+'" category name already exists!'))
            return redirect('create-category')

        newCategory = Category.objects.create(name=name, description=description)
        newCategory.save()
        slug_str = "%s" % (newCategory.name)
        newCategory.slug = slugify(slug_str)
        newCategory.save()
        messages.success(request,'New Category "'+name+'" Created Successfully!')
        return redirect('category-list')

    context = {
                'task': task,
                'manager':manager,
            }
    return render(request, 'manager/create_category.html', context)


def updateCategory(request,slug):
    task = "Update"
    manager  = Manager.objects.get(username=request.user)
    category = Category.objects.get(slug=slug)

    form = CategoryForm(instance=category)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request,'Category "'+category.name+'" Updated Successfully!')
            return redirect('category-list')

    context = {
                'task': task,
                'form':form,
                'manager':manager,
            }
    return render(request, 'manager/update_category.html', context)


def deleteCategory(request,slug):
    category = Category.objects.get(slug=slug)
    name = category.name
    if request.method == 'POST':
        category.delete()
        messages.success(request,'Category "'+name+'" Deleted Successfully!')
        return redirect('category-list')
    
    context = {'object':category}
    return render(request, 'temp/delete_object.html', context)