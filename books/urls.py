from django.urls import path
from .views import *

urlpatterns = [
    path('', books_view, name='books_home'),
    path('post-book/', post_book_view, name='post_book'),
    # path('update-book/<str:pk>', update_book_view, name='update-book'),
    path('details/<str:slug>/', book_details_view, name='book_details'),
]
