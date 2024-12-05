from django.contrib import admin
from django.urls import path,include

from Accounts import urls as A_URLS

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include(A_URLS)),

]
