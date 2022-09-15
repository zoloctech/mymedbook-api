from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
# from .models import City,State,Area
import datetime
from django.utils import timezone
from admins.models import Location

# Create your models here.
class Roles(models.Model):
    role = models.CharField(max_length=100)
    is_del = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name





class UserManager(BaseUserManager):
    def create_user(self, phone,password=None, is_staff=False, is_active=True, is_superuser=False):
        if not phone:
            raise ValueError('users must have a phone number')

        if not password:
            raise ValueError('users must have a password')
        

        user_obj = self.model(phone=phone)
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.active = is_active
        user_obj.super = is_superuser
       

        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, phone, password=None):
        user = self.create_user(phone,password=password,is_staff=True,)
        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,
            is_superuser=True,
        )
        return user



class User(AbstractBaseUser):
    VARIFIED_CHOICES = (("phone", "phone"), ("email", "email"))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Up to 15 digits allowed.")
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, null=True, blank=True)
    fname = models.CharField(max_length=50, blank=True, null=True)
    lname = models.CharField(max_length=50, blank=True, null=True)      
    phone = models.CharField(validators=[phone_regex], max_length=15, unique=True)
    email=models.EmailField(blank=False, null=False, unique=True)
    address = models.TextField(max_length=500, blank=True, null=True)
    
    postcode = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=200)
    # last_login = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    # first_login = models.DateTimeField(default=timezone.now())
    email_otp = models.CharField(max_length=9, blank=True, null=True)
    phone_otp = models.CharField(max_length=9, blank=True, null=True)
    count_otp = models.IntegerField(default=0, help_text='Number of otp sent')
    is_verified = models.BooleanField(default=False)
    verified_chioce = models.CharField(max_length=100, choices=VARIFIED_CHOICES, help_text='If otp verification got successful', default="phone")
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    super = models.BooleanField(default=False)
    is_del = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True,related_name='state')
    city = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True,related_name='city')
    area = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True,related_name='area')

    # location_id=models.ForeignKey(Location, to_fields=['state_id', 'city_id','area_id'], related_name='abc', on_delete=models.CASCADE)

  
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone

    def get_full_name(self):
        return self.fname + " " + self.lname

    def get_short_name(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):

        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_superuser(self):
        return self.super

class TempData(models.Model):
    CATEGORY_CHOICES = (("registration", "registration"), ("edit_profile","edit_profile"),("login","login"))
    VARIFIED_CHOICES = (("phone", "phone"), ("email", "email"))
    section = models.CharField(max_length=100, choices=CATEGORY_CHOICES, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Up to 15 digits allowed.")
    phone_or_email = models.CharField(max_length=100, choices=VARIFIED_CHOICES ,default="phone")
    email=models.EmailField(blank=False, null=True, unique=True)
    phone = models.CharField(validators=[phone_regex], max_length=15,null=True ,unique=True)
    phone_otp = models.CharField(max_length=9, blank=True, null=True)
    email_otp = models.CharField(max_length=9, blank=True, null=True)
    phone_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    is_del = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    
    
    def __str__(self):
        return f"{self.phone}  {self.email}"

    @property
    def delete_after_ten_minutes(self):
        time = self.created_at + datetime.timedelta(minutes=10)
        if time < datetime.datetime.now():
            self.delete()
            return True
        return False
