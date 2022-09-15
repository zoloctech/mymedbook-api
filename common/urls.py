from django.urls import path
from . import views
from rest_framework import routers
from django.urls import include


urlpatterns = [


    path('get-otp', views.GetOTP.as_view(), name='get_otp'),
    path('verify-otp', views.VerifyOTP.as_view(), name='verify_phone_otp'),
    path('change-password', views.ChangePassword.as_view(), name='change_password'),
]
