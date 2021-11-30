from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.text import slugify
from .forms import *

def books_view(request):
    books = Book.objects.all()
    latest_books = Book.objects.all()[:3]

    categories = Category.objects.all()
    context = {
        'books': books,
        'latest_books': latest_books,
        'categories': categories,
    }
    return render(request, "books/books_home.html", context)


@login_required
def post_book_view(request):
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
            return redirect('books_home')
        else:
            print("Error: Form Invalid")
            print(form.errors)
            context = {
                'task': task,
                'form': form,
            }
            return render(request, 'books/post_update_book.html', context)

    context = {
        'task': task,
        'form': form,
    }

    return render(request, 'books/post_update_book.html', context)


@login_required
def book_details_view(request, slug):
    book = Book.objects.get(slug=slug)
    context = {
        'book': book
    }
    return render(request, "books/book_details.html", context)
