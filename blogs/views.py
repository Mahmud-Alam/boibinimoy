from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify

#from .filters import *
from .forms import *
from users.decorators import *
from users.models import *
from books.models import *


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','manager'])
def blogs_home(request):
    manager=customer=0
    user = User.objects.get(username=request.user)
    if user.groups.all()[0].name == 'manager':
        manager = Manager.objects.get(username=request.user)
    elif user.groups.all()[0].name == 'customer':
        customer = Customer.objects.get(username=request.user)

    blogs = Blog.objects.order_by('-created')
    manager_blogs = []
    for blog in blogs:
        if blog.creator.groups.all()[0].name == 'manager':
            manager_blogs.append(blog)
    
    latest_manager_blogs = manager_blogs

    all_customer = Customer.objects.all()
    all_manager = Manager.objects.all()
    latest_books = Book.objects.order_by('-created')[:5]
    categories = Category.objects.order_by('name')
    category_count = categories.count()
    cat_book_count = [Book.objects.filter(category=cat).count() for cat in categories]
    category_dict =  zip(categories,cat_book_count) 
    category_dict = sorted(category_dict, key = lambda t: t[1], reverse=True)

    # Comment Part
    commentForm = BlogCommentForm()
    if request.method == 'POST':
        commentForm = BlogCommentForm(request.POST, request.FILES)
        if commentForm.is_valid():
            obj = commentForm.save()
            obj.creator = user
            obj.save()

    context = {'manager':manager,'customer':customer,'all_customer':all_customer,'all_manager':all_manager,'commentForm':commentForm,'blogs':blogs,'manager_blogs':manager_blogs,'latest_books':latest_books,'latest_manager_blogs':latest_manager_blogs,'category_dict':category_dict,'category_count':category_count}
    return render(request, "blogs/blogs_home.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','manager'])
def blogs_home_manager(request):
    manager=customer=0
    user = User.objects.get(username=request.user)
    if user.groups.all()[0].name == 'manager':
        manager = Manager.objects.get(username=request.user)
    elif user.groups.all()[0].name == 'customer':
        customer = Customer.objects.get(username=request.user)

    blogs = Blog.objects.order_by('-created')
    manager_blogs = []
    for blog in blogs:
        if blog.creator.groups.all()[0].name == 'manager':
            manager_blogs.append(blog)
    
    all_manager = Manager.objects.all()
    latest_manager_blogs = manager_blogs

    latest_books = Book.objects.order_by('-created')[:5]
    categories = Category.objects.order_by('name')
    category_count = categories.count()
    cat_book_count = [Book.objects.filter(category=cat).count() for cat in categories]
    category_dict =  zip(categories,cat_book_count) 
    category_dict = sorted(category_dict, key = lambda t: t[1], reverse=True)

    context = {'manager':manager,'all_manager':all_manager,'customer':customer,'blogs':blogs,'manager_blogs':manager_blogs,'latest_books':latest_books,'latest_manager_blogs':latest_manager_blogs,'category_dict':category_dict,'category_count':category_count}
    return render(request, "blogs/blogs_home_manager.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['manager','customer'])
def create_blog(request):
    user = User.objects.get(username=request.user)
    manager=customer=0
    
    if user.groups.all()[0].name == 'manager':
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

            if user.groups.all()[0].name == 'manager':
                return redirect('manager-dashboard', username = request.user)
            elif user.groups.all()[0].name == 'customer':
                return redirect('user-profile', username = request.user)

    context = {
        'task': task,
        'form': form,
        'manager':manager,
        'customer':customer,
    }

    return render(request, 'blogs/create_blog_post.html', context)
