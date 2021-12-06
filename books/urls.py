from django.urls import path
from .views import *

urlpatterns = [
    path('', books_home, name='books-home'),
    path('create-post/', create_post, name='create-post'),
    path('update-post/<str:pk>/', update_post, name='update-post'),
    path('details/<str:slug>/', books_details, name='books-details'),
    path('delete-post/<str:pk>/', delete_post, name='delete-post'),
    path('category/<str:slug>/', books_category, name='books-category'),
]
