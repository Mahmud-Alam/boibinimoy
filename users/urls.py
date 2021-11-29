from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='home'),
    path('register/', views.registrationPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('account-activate/<uidb64>/<token>/', views.accountActivate, name='account-activate'),
    path('profile/', views.userProfile, name='user-profile'),
    path('edit-profile/', views.editUserProfile, name='edit-user-profile'),
    path('change-username/', views.changeUsername, name='change-username'),
    path('change-username-confirm/<uidb64>/<token>/<username>/', views.changeUsernameConfirm, name='change-username-confirm'),
    path('change-email/', views.changeEmail, name='change-email'),
    path('change-email-confirm/<uidb64>/<token>/<email>/', views.changeEmailConfirm, name='change-email-confirm'),
]
