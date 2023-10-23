from django.urls import include, path
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),

    path('password-change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/auth-password-change-done.html'
    ), name="password_change_done"),

    path('password-reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', UserPasswrodResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/auth-password-reset-done.html'
    ), name='password_reset_done'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/auth-password-reset-complete.html'
    ), name='password_reset_complete'),
    path('profile/', profile, name='profile'),

]
