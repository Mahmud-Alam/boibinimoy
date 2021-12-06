from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify

from .filters import *
from .forms import *
from users.decorators import *


@login_required(login_url='login')
def books_home(request):
    books = Book.objects.all()
    latest_books = Book.objects.all()[:5]
    categories = Category.objects.all()

    bookFilter = BookFilter(request.GET, queryset=books)
    books = bookFilter.qs

    context = {'books':books,'latest_books':latest_books,'categories':categories,'bookFilter':bookFilter}
    return render(request, "books/books_home.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def create_post(request):
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
            }
            return render(request, 'books/create_book_post.html', context)

    context = {
        'task': task,
        'form': form,
    }

    return render(request, 'books/create_book_post.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def update_post(request,pk):
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
            }
            return render(request, 'books/create_book_post.html', context)

    context = {
        'task': task,
        'form': form,
    }

    return render(request, 'books/create_book_post.html', context)


@login_required(login_url='login')
def books_details(request, slug):
    book = Book.objects.get(slug=slug)
    customer = Customer.objects.get(username=book.creator.username)
    
    if request.user == customer.username:
        flag=True
    else:
        flag=False

    
    context = {'book': book,'flag':flag}
    return render(request, "books/books_details.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
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


@login_required(login_url='login')
def books_category(request,slug):
    category = Category.objects.get(slug=slug)
    books = Book.objects.filter(category=category)
    all_categories = Category.objects.all()

    bookFilter = BookFilter(request.GET, queryset=books)
    books = bookFilter.qs

    context = {'books': books,'category':category,'categories':all_categories,'bookFilter':bookFilter}
    return render(request, "books/books_category.html", context)



