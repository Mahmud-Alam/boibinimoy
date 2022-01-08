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

    path('admin-panel/<str:username>/', views.adminPanel, name='admin-panel'),
    path('admin-profile/<str:username>/', views.adminProfile, name='admin-profile'),
    path('edit-admin-profile/', views.editAdminProfile, name='edit-admin-profile'),
    path('create-admin/', views.createAdmin, name='create-admin'),
    path('create-manager/', views.createManager, name='create-manager'),
    path('manage-administrators/', views.manageAdministrators, name='manage-administrators'),

    path('manager-dashboard/<str:username>/', views.managerDashboard, name='manager-dashboard'),
    path('manager-profile/<str:username>/', views.managerProfile, name='manager-profile'),
    path('edit-manager-profile/', views.editManagerProfile, name='edit-manager-profile'),
    path('manage-customers/', views.manageCustomers, name='manage-customers'),
    path('create-category/', views.createCategory, name='create-category'),
    path('update-category/<str:slug>/', views.updateCategory, name='update-category'),
    path('delete-category/<str:slug>/', views.deleteCategory, name='delete-category'),
    path('category-list/', views.categoryList, name='category-list'),
    path('pending-post/', views.pendingPost, name='pending-post'),

    path('delete-user/<str:username>/', views.deleteUser, name='delete-user'),
    path('reactive-user/<str:username>/', views.reactiveUser, name='reactive-user'),


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