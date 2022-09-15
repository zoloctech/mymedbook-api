from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.hell),
    path('create/', views.CreateCalendarEventAPIView.as_view()),
]
