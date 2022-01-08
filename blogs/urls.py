from django.urls import path
from .views import *

urlpatterns = [
    path('', blogs_home, name='blogs-home'),
    path('manager', blogs_home_manager, name='blogs-home-manager'),
    path('create-blog/', create_blog, name='create-blog'),
    path('update-blog/<str:pk>/', update_blog, name='update-blog'),
    path('delete-blog/<str:pk>/', delete_blog, name='delete-blog'),
    path('accept-blog/<str:pk>/', accept_blog, name='accept-blog'),
    path('accept-book/<str:pk>/', accept_book, name='accept-book'),
    # path('details/<str:slug>/', books_details, name='books-details'),
    # path('category/<str:slug>/', books_category, name='books-category'),
]
