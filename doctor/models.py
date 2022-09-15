from django.db import models
from admins.models import Qualification, Speciality
from users.models import User
# Create your models here.




class Doctor(models.Model):
    
    def get_upload_path(instance, filename):
        return 'documents/{0}/{1}'.format(instance.clinic_name, filename)

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
    registration_number = models.CharField(max_length=255, blank=True, null=True)
    specilization_id = models.ForeignKey(Speciality, on_delete=models.CASCADE, blank=True, null=True)
    qualification_id = models.ForeignKey(Qualification, on_delete=models.CASCADE, blank=True, null=True)
    clinic_name = models.CharField(max_length=255, blank=True, null=True)
    clinic_registration_number = models.CharField(max_length=255, blank=True, null=True)
    digital_signature = models.ImageField(upload_to="images/", blank=True, null=True)
    address_proof_of_clinic_regetration = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    degree_certificate = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    doctor_regestration_no_proof = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    clinic_regestration_certificate = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    document1 = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    document2 = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    document3 = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    document4 = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    bio = models.TextField(max_length=300,blank=True, null=True)
    experience_years = models.IntegerField(default=0,blank=True, null=True)
    is_del = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fee = models.IntegerField(default=200)
    timeslot = models.IntegerField(default=15)
    def __str__(self):
        return f"{self.clinic_name}"



class DoctorRatingReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    rating = models.FloatField()
    review = models.CharField(max_length=1000)
    is_del = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.rating}"

class DoctorTiming(models.Model): 
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_date=models.DateField('start date')
    end_date=models.DateField('end date')
    start_time=models.TimeField('start Time')
    end_time=models.TimeField('end Time')
    is_del = models.BooleanField(default=False)
    is_in_schedul=models.BooleanField(default=False)

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    start_date=models.DateField('start date')
    end_date=models.DateField('end date')
    start_time=models.TimeField('start Time')
    end_time=models.TimeField('end Time')
    is_del = models.BooleanField(default=False)
    is_done_appointment=models.BooleanField(default=False)

class BookAppointment(models.Model):
    MODE_CHOICES = (("offline", "offline"), ("online","online"))
    appointment_mode = models.CharField(max_length=100, choices=MODE_CHOICES, null=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,null=True)
    
    start_date = models.DateField('start date')
    end_date = models.DateField('end date',null=True)
    start_time = models.TimeField('start Time')
    end_time = models.TimeField('end Time',null=True) 
    meeting_link = models.URLField(max_length=200, blank=True,null=True)
    is_del = models.BooleanField(default=False)
