from django.urls import path 
from .import views
from django.contrib.auth import views as auth_views
urlpatterns =[
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-account/',views.create_account,name='create_account'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('transactions/', views.transaction_history, name='transactions'),
    path('transfer/', views.transfer, name='transfer'),
    path('profile/', views.profile, name="profile"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('change-password/', views.change_password , name='change_password'),
    path('logout/', views.logout_view, name='logout'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path(
    "forgot-password/",
    auth_views.PasswordResetView.as_view(
        template_name="forgot_password.html"
    ),
    name="forgot_password"
),

path(
    "password-reset/done/",
    auth_views.PasswordResetDoneView.as_view(
        template_name="password_reset_done.html"
    ),
    name="password_reset_done"
),

path(
    "password-reset/<uidb64>/<token>/",
    auth_views.PasswordResetConfirmView.as_view(
        template_name="password_reset_confirm.html"
    ),
    name="password_reset_confirm"
),

path(
    "password-reset/complete/",
    auth_views.PasswordResetCompleteView.as_view(
        template_name="password_reset_complete.html"
    ),
    name="password_reset_complete"
),
]

    
