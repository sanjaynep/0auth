from django.urls import include, path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('login/', login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/', password_reset, name='password_reset'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('password-reset-confirm/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),  # For forgot password
]


