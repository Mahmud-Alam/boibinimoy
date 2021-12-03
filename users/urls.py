from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.homePage, name='home'),
    path('register/', views.registrationPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('account-activate/<uidb64>/<token>/', views.accountActivate, name='account-activate'),
    path('profile/<str:username>/', views.userProfile, name='user-profile'),
    path('edit-profile/', views.editUserProfile, name='edit-user-profile'),
    path('change-username/', views.changeUsername, name='change-username'),
    path('change-username-confirm/<uidb64>/<token>/<username>/', views.changeUsernameConfirm, name='change-username-confirm'),
    path('change-email/', views.changeEmail, name='change-email'),
    path('change-email-confirm/<uidb64>/<token>/<email>/', views.changeEmailConfirm, name='change-email-confirm'),
    path('change-password/', views.changePassword, name='change-password'),

    # for email password reset with django template
    # path('reset-password/',auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('reset-password-sent/',auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset-password-complete/',auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]


"""
from the documentation: https://docs.djangoproject.com/en/3.2/topics/auth/default/#all-authentication-views
1 - Submit email form                           PasswordResetView.as_view()
2 - Email sent success message                  PasswordResetDoneView.as_view()
3 - Link to password Reset from in email        PasswordResetConfirmView.as_view()
4 - Password successfully changed message       PasswordResetCompleteView.as_view()
"""