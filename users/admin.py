from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from users.models import Roles, TempData
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin


User = get_user_model()
# register your models here.


class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'role']
    search_fields = ['role']
    list_filter = ['id', 'role']
    ordering = ['role']

    class Meta:
        model = Roles


class TempDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone', 'email']
    search_fields = ['phone', 'email']
    list_filter = ['id', 'phone', 'email']
    ordering = ['phone']

    class Meta:
        model = TempData


class UserAdmin(BaseUserAdmin):

    list_display = ('id', 'fname', 'lname', 'phone', 'email', 'role_id',)
    list_ordering = ['-id']
    list_filter = ('staff', 'active', 'role_id')
    fieldsets = (
        (None, {'fields': ('phone', 'phone_otp', 'email','email_otp')}),
        ('Personal info', {'fields': ('fname', 'lname', 'address','state','city','area')}),
        ('Permissions', {'fields': ('staff', 'active', 'super',
          )}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'phone_otp')}
         ),
    )

    search_fields = ('phone', 'fname', 'role_id')
    ordering = ('phone', 'fname', 'id')
    filter_horizontal = ()

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


admin.site.register(User, UserAdmin)
admin.site.register(Roles, RoleAdmin)
admin.site.register(TempData, TempDataAdmin)
# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
