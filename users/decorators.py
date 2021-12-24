from django.contrib.auth import decorators
from django.shortcuts import redirect, render

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return  redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)

            else: 
                return render(request,'users/unauthorized_page.html')

        return wrapper_func
    return decorator


def visitors_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        
        if group == 'admin':
            return redirect('admin-panel',username = request.user)
            
        if group == 'manager':
            return redirect('manager-dashboard',username = request.user)

        if group == 'customer':
            return redirect('user-profile',username = request.user)
        
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func