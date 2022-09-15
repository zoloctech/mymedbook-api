from django.db import models
from django.utils.text import slugify
from django.db import models

# Create your models here.
class Location(models.Model):
    CATEGORY_CHOICES = (("taluk", "taluk"), ("village","village"), ("district", "district"))
    LOCATION_CHOICES = (("state", "state"), ("city", "city"), ("area", "area"))
    name = models.CharField(max_length=100)
    slug = models.SlugField(default='',editable=False)
    section = models.CharField(max_length=100, choices=LOCATION_CHOICES, default="state")
    is_del = models.BooleanField(default=False)
    is_cat = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    area_section = models.CharField(max_length=100, choices=CATEGORY_CHOICES, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self,*args,**kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.name



class Speciality(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(default='',editable=False)
    icon = models.ImageField(upload_to="images/", blank=True, null=True)
    is_del = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Qualification(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    is_del = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_queryset(self):
        qs = super(Qualification, self).get_queryset()
        if self.is_del:
            qs = qs.exclude(is_del=False)
            return qs

    def __str__(self):
        return self.name

