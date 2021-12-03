from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.text import slugify

from .filters import *
from .forms import *

def books_home(request):
    books = Book.objects.all()
    latest_books = Book.objects.all()[:3]
    categories = Category.objects.all()

    bookFilter = BookFilter(request.GET, queryset=books)
    books = bookFilter.qs

    context = {'books':books,'latest_books':latest_books,'categories':categories,'bookFilter':bookFilter}
    return render(request, "books/books_home.html", context)


@login_required
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


@login_required
def books_details(request, slug):
    book = Book.objects.get(slug=slug)
    
    customer = Customer.objects.get(username=book.creator.username)
    if request.user == customer.username:
        flag=True
    else:
        flag=False

    print('_______________',customer,flag)
    context = {'book': book,'flag':flag}
    return render(request, "books/books_details.html", context)
