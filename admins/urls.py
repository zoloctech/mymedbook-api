from django.urls import path
from . import views



# Create your urls here.
urlpatterns = [
    #	location
    path('view-all-doctors-location', views.GetLocationAPIView.as_view(), name='get_doctors_location'),
    path('all-doctor-reviews',views.GetAllReviewAPI.as_view(),name='all_doctor_reviews'),
    path('create-doctors-location', views.CreateLocationAPIView.as_view(), name='create_location'),
    path('edit-doctors-location', views.UpdateLocationAPIView.as_view(), name='edit_doctors_location'),
    path('delete-doctors-location', views.DeleteLocationAPIView.as_view(), name='delete_doctors_location'),
    path('block-verify',views.BlockVerifyAPIView.as_view(),name="blcked_verify_user"),
    path('block-review',views.BlockRatingAPI.as_view(),name='blcok_review'),
    #doctor_specialities
    path('view-all-doctors-speciality', views.SpecialityAPIView.as_view(), name='view_all_doctors_speciality'),
    path('create-doctors-speciality', views.CreateSpecialityAPIView.as_view(),
         name='create_doctors_speciality'),
    path('edit-doctors-speciality',
         views.UpdateSpecialityAPIView.as_view(), name='edit_doctors_speciality'),
    path('delete-doctors-speciality',
         views.DeleteSpecialityAPIView.as_view(), name='delete_doctors_speciality'),
     path('view-doctors-speciality',views.OneSpecialityAPIView.as_view(),name='view_doctors_speciality'),
     path('view-doctors-location',views.OneLocationAPIView.as_view(),name='view_doctors_location'),
     path('view-doctors-qualification',views.OneQualificationAPIView.as_view(),name='view_doctors_qualification'),

    #doctor_qualifications
    path('create-doctors-qualification', views.CreateQualificationAPIView.as_view(),
         name='create_doctors_qualification'),
    path('view-all-doctors-qualification', views.GetQualificationsAPIView.as_view(),
         name='view_all_doctors_qualification'),
    path('edit-doctors-qualification',
         views.UpdateQualificationAPIView.as_view(), name='edit_doctors_qualification'),
    path('delete-doctors-qualification',
         views.DeleteQualificationAPIView.as_view(), name='delete_doctors_qualification'), 
    
    ]