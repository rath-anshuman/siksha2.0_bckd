from django.urls import path,include
from Accounts import urls as A_URLS

from .views import login,logout,send_otp_email,signup

urlpatterns = [
    path('login/',login),
    path('logout/',logout),
    path('send_otp/',send_otp_email),
    path('signup/',signup)

]
