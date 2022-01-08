from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify

from .filters import *
from .forms import *
from users.decorators import *
from users.models import *
from blogs.models import *


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','manager'])
def books_home(request):
    manager=customer=0
    user = User.objects.get(username=request.user)
    if user.groups.all()[0].name == 'manager':
        manager = Manager.objects.get(username=request.user)
    elif user.groups.all()[0].name == 'customer':
        customer = Customer.objects.get(username=request.user)

    all_customer = Customer.objects.all()
    all_manager = Manager.objects.all()
    pending_blog_posts = Blog.objects.filter(review='False').order_by('-created')
    pending_book_posts = Book.objects.filter(review='False').order_by('-created')

    books = Book.objects.order_by('-created')
    latest_books = Book.objects.filter(review='True').order_by('-created')[:5]
    categories = Category.objects.order_by('name')
    category_count = categories.count()
    cat_book_count = [Book.objects.filter(category=cat).count() for cat in categories]
    category_dict =  zip(categories,cat_book_count) 
    category_dict = sorted(category_dict, key = lambda t: t[1], reverse=True)

    bookFilter = BookFilter(request.GET, queryset=books)
    books = bookFilter.qs
    books_count = books.count()

    # Comment Part
    commentForm = BookCommentForm()
    if request.method == 'POST':
        bookName = request.POST.get('bookName')
        book = Book.objects.get(name = bookName)
        commentForm = BookCommentForm(request.POST, request.FILES)
        if commentForm.is_valid():
            obj = commentForm.save()
            obj.creator = user
            obj.book = book
            obj.save()
            return redirect('books-home')
    
    context = {'books':books,'latest_books':latest_books,'bookFilter':bookFilter,'books_count':books_count,'category_count':category_count,
                'category_dict':category_dict,'customer':customer,'manager':manager,'all_customer':all_customer,'all_manager':all_manager,
                'commentForm':commentForm,'pending_blog_posts':pending_blog_posts,'pending_book_posts':pending_book_posts}
    return render(request, "books/books_home.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def create_post(request):
    customer = Customer.objects.get(username=request.user)
    task = "Post New"
    form = BookForm()

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save()
            current_user = request.user
            obj.creator = Customer.objects.get(username=current_user)
            slug_str = "%s %s" % (obj.name, obj.id)
            obj.slug = slugify(slug_str)
            obj.save()
            full_name = request.user.first_name+' '+request.user.last_name
            messages.success(request,'Congratulations "'+full_name+'"! Your have created a post!')
            return redirect('user-profile', username = request.user)
        else:
            print("Error: Form Invalid")
            print(form.errors)
            context = {
                'task': task,
                'form': form,
                'customer':customer,
            }
            return render(request, 'books/create_book_post.html', context)

    context = {
        'task': task,
        'form': form,
        'customer':customer,
    }

    return render(request, 'books/create_book_post.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def update_post(request,pk):
    customer = Customer.objects.get(username=request.user)
    task = "Update"
    book = Book.objects.get(id=pk)
    form = BookForm(instance=book)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)

        if form.is_valid():
            obj = form.save()
            # current_user = request.user
            # obj.creator = Customer.objects.get(username=current_user)
            slug_str = "%s %s" % (obj.name, obj.id)
            obj.slug = slugify(slug_str)
            obj.save()
            full_name = request.user.first_name+' '+request.user.last_name
            messages.success(request, full_name+', your post updated successfully!')
            return redirect('user-profile', username = request.user)
        else:
            print("Error: Form Invalid")
            print(form.errors)
            context = {
                'task': task,
                'form': form,
                'customer':customer,
            }
            return render(request, 'books/create_book_post.html', context)

    context = {
        'task': task,
        'form': form,
        'customer':customer,
    }

    return render(request, 'books/create_book_post.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','manager'])
def books_details(request, slug):
    # customer = Customer.objects.get(username=request.user)
    # main_user = User.objects.get(username=username)
    customer = manager = 0
    if request.user.groups.all()[0].name == 'manager':
        manager  = Manager.objects.get(username=request.user)
    elif request.user.groups.all()[0].name == 'customer':
        customer = Customer.objects.get(username=request.user)

    book = Book.objects.get(slug=slug)
    customerInfo = Customer.objects.get(username=book.creator.username)
    
    if request.user == customerInfo.username:
        flag=True
    else:
        flag=False

    all_customer = Customer.objects.all()
    all_manager = Manager.objects.all()
    pending_blog_posts = Blog.objects.filter(review='False').order_by('-created')
    pending_book_posts = Book.objects.filter(review='False').order_by('-created')
    
    # Comment Part
    commentForm = BookDetailsCommentForm()
    if request.method == 'POST':
        bookName = request.POST.get('bookName')
        book = Book.objects.get(name = bookName)
        commentForm = BookDetailsCommentForm(request.POST, request.FILES)
        if commentForm.is_valid():
            obj = commentForm.save()
            obj.creator = request.user
            obj.book = book
            obj.save()
            return redirect('books-details',book.slug)

    context = {'book': book,'flag':flag,'customer':customer,'manager':manager,'all_customer':all_customer,'all_manager':all_manager,
                'commentForm':commentForm,'pending_blog_posts':pending_blog_posts,'pending_book_posts':pending_book_posts}
    return render(request, "books/books_details.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','manager'])
def delete_post(request,pk):
    book = Book.objects.get(id=pk)
    title = "Delete Post"
    text1 = "delete post"

    if request.method == 'POST':
        book.delete()
        full_name = request.user.first_name+' '+request.user.last_name
        messages.success(request, full_name+', your post deleted!')
        return redirect('user-profile', username = request.user)

    context = {'book':book,'title':title,'text1':text1}
    return render(request,"books/delete_book_post.html",context)


@allowed_users(allowed_roles=['customer','manager'])
@login_required(login_url='login')
def books_category(request,slug):
    customer = manager = 0
    if request.user.groups.all()[0].name == 'manager':
        manager  = Manager.objects.get(username=request.user)
    elif request.user.groups.all()[0].name == 'customer':
        customer = Customer.objects.get(username=request.user)
    
    category = Category.objects.get(slug=slug)
    books = Book.objects.filter(category=category).order_by('-created')
    categories = Category.objects.order_by('name')
    category_count = categories.count()
    cat_book_count = [Book.objects.filter(category=cat).count() for cat in categories]
    pending_blog_posts = Blog.objects.filter(review='False').order_by('-created')
    pending_book_posts = Book.objects.filter(review='False').order_by('-created')

    category_dict =  zip(categories,cat_book_count) 
    category_dict = sorted(category_dict, key = lambda t: t[1], reverse=True)

    bookFilter = BookFilter(request.GET, queryset=books)
    books = bookFilter.qs
    books_count = books.count()

    context = {'books': books,'category':category,'category_dict':category_dict,'bookFilter':bookFilter,'books_count':books_count,
                'category_count':category_count,'customer':customer,'manager':manager,'pending_blog_posts':pending_blog_posts,'pending_book_posts':pending_book_posts}
    return render(request, "books/books_category.html", context)



