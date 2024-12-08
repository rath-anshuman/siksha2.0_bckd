from django.urls import path,include
from Accounts import urls as A_URLS

from .views import login,logout,send_otp_login,send_otp_signup,signup

urlpatterns = [
    path('send_otp_signup/',send_otp_signup),
    path('send_otp_login/',send_otp_login),
    path('login/',login),
    path('signup/',signup),
    path('logout/',logout),
]
