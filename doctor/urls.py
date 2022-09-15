from django.urls import path, include
from .import views
from rest_framework.routers import DefaultRouter
from django.views.decorators.csrf import csrf_exempt


# Create a router and register our viewsets with it.
urlpatterns = [
    path('doctor-registration/', csrf_exempt(views.CreateDoctorAPIView.as_view()), name="doctor_registration"),
    path('get-doctor/<int:pk>/', views.GetDoctorAPIView.as_view(), name="get_doctor"),
    path('view-all-doctors', views.ViewAllDoctorsAPIView.as_view(),name="view_all_doctors"),
    path('edit-doctor/', views.editdoctor, name='edit'),
    path('take-appointment/', views.TakeAppointment.as_view()),
    path('doctor-schedul/', views.DoctorCalandarSchedule.as_view()),
    path('book-appointment/', views.BookAnAppointmentList.as_view(),name='appointment-list'),
    path('book/', views.BookAppointmentList.as_view(), name='appointment-detail'),
    path('create/', views.CreateCalendarEventAPIView.as_view()),
    path('get-qualification-doctor/', views.GetQualificationDoctorAPIView.as_view()),
    path('get-speciality-doctor/', views.GetSPecializationDoctorAPIView.as_view()),



]
