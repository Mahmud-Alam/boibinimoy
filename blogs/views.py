from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify

#from .filters import *
from .forms import *
from users.decorators import *
from users.models import *


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def blogs_home(request):
    context = {}
    return render(request, "blogs/blogs_home.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','manager','customer'])
def create_blog(request):
    user = User.objects.get(username=request.user)
    admin=manager=customer=0
    if user.groups.all()[0].name == 'admin':
        admin = Admin.objects.get(username=request.user)
    elif user.groups.all()[0].name == 'manager':
        manager = Manager.objects.get(username=request.user)
    elif user.groups.all()[0].name == 'customer':
        customer = Customer.objects.get(username=request.user)

    task = "Post New"
    form = BlogForm()

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save()
            obj.creator = user
            if user.groups.all()[0].name == 'customer':
                obj.review = "False"
            slug_str = "%s %s" % (obj.title, obj.id)
            obj.slug = slugify(slug_str)
            obj.save()
            full_name = user.first_name+' '+user.last_name
            messages.success(request,'"'+full_name+'", your blog post created successfully!')

            if user.groups.all()[0].name == 'admin':
                return redirect('admin-panel', username = request.user)
            elif user.groups.all()[0].name == 'manager':
                return redirect('manager-dashboard', username = request.user)
            elif user.groups.all()[0].name == 'customer':
                return redirect('user-profile', username = request.user)
        else:
            print("Error: Form Invalid")
            print(form.errors)
            context = {
                'task': task,
                'form': form,
                'admin':admin,
                'manager':manager,
                'customer':customer,
            }
            return render(request, 'blogs/create_blog_post.html', context)

    context = {
        'task': task,
        'form': form,
        'admin':admin,
        'manager':manager,
        'customer':customer,
    }

    return render(request, 'blogs/create_blog_post.html', context)
