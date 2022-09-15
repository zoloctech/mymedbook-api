from django.urls import path
from . import views
from rest_framework import routers
from django.urls import include


urlpatterns = [
    path('role', views.RoleAPIView.as_view(), name='role'),
    path('create-rating',views.CreateRatingAPI.as_view(),name='create_rating'),
    path('edit-rating',views.EditRating,name = 'edit_rating'),
    path('temp-data', views.TempDataAPIView.as_view(), name='temp_data'),
    #path('get-register-otp-mobile/', views.ValidateSendPhoneOTP.as_view(), name='send_phone_otp'),
    path('logout',views.UserLogoutAPIView.as_view(),name="logout"),
    path('user-registration/', views.SignUpAPI.as_view(), name='user_registration'),
    path('view-all-users',views.GetUsersAPIView.as_view(),name='view_all_users'),
    path('get-login-otp-mobile',views.LoginPhoneSendAPI.as_view(), name='send_phone_otp'),
    path('verify-login-otp-mobile',views.LoginPhoneVerifyAPI.as_view(), name='verify_phone_otp'),
    path('get-user', views.GetAuthUserAPIView.as_view(), name='get_user'),
    path('edit-user',views.edituser,name='edit')
    
]