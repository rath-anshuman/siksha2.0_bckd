from django.urls import path,include
from Accounts import urls as A_URLS

from .views import login,send_otp_email,signup

urlpatterns = [
    path('login/',login),
    path('send_otp/',send_otp_email),
    path('signup/',signup)

]
