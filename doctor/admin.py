from re import A
from django.contrib import admin
from doctor.models import Doctor,DoctorRatingReview,DoctorTiming,Appointment, BookAppointment
# Register your models here.


# Register your models here.    
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id']
    search_fields = ['specilization']

@admin.register(DoctorRatingReview)
class DoctorRatingReviewAdmin(admin.ModelAdmin):
    list_display = ['id','user','doctor','rating','review']
    search_fields = ['rating']


@admin.register(DoctorTiming)
class DoctorTimingAdmin(admin.ModelAdmin):
    list_display = ['id','doctor','is_del']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    lsit_display = ['id','doctor','user','doctortiming','appointment_startdatetime','appointment_enddatetime','is_del']

@admin.register(BookAppointment)
class BookAppointmentAdmin(admin.ModelAdmin):
    list_display = ['id','doctor','patient','appointment_mode','start_date', 'end_date','start_time', 'end_time', 'is_del','meeting_link']