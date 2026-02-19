from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_approved', 'is_staff')
    list_filter = ('role', 'is_approved', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Roles', {'fields': ('role', 'is_approved', 'phone_number')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Roles', {'fields': ('role', 'is_approved', 'phone_number')}),
    )

admin.site.register(User, CustomUserAdmin)
