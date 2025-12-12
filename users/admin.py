from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User  # مدل کاربر خودتان را ایمپورت کنید

class UserAdmin(BaseUserAdmin):
    # 1. Update list_display to show more columns
    ordering = ['phone_number']
    list_display = ['phone_number', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
    
    # 2. Update fieldsets to include the Personal Info section
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),  # Add this back
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password'),
        }),
    )

admin.site.register(User, UserAdmin)