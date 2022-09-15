from django.contrib import admin
from .models import Location
# Register your models here.

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_del', 'created_at', 'updated_at')
    # list_filter = ('is_del',)
    # search_fields = ('name','id')
    # ordering = ('id',)