from django.contrib import admin
from django.urls import path,include
from .views import home, login_attempt, register, token_send, success, verify, error_page

urlpatterns = [
    path('', home, name = "home"),
    path('login/', login_attempt, name = 'login'),
    path('register/', register , name = 'register_attempt'),
    path('token/', token_send , name = 'token_send'),
    path('success/', success , name = 'success'),
    path('verify/<auth_token>', verify , name = 'verify'),
    path('error>', error_page , name = 'error'),
]