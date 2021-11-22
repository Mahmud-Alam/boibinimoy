from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='home'),
    path('register/', views.registrationPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('account-activate/<uidb64>/<token>/', views.accountActivate, name='account-activate'),
    path('profile/', views.userProfile, name='user-profile'),
    path('edit-profile/', views.editProfile, name='edit-profile'),
]
