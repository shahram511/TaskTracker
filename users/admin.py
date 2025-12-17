from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile
from django.db import models


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'
    fk_name = 'user'
    extra = 0
    fields = ['avatar', 'bio', 'created_at']
    readonly_fields = ['created_at']

    
class UserAdmin(BaseUserAdmin):
    ordering = ['phone_number']
    list_display = ['phone_number', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
    inlines = [ProfileInline]
    
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),  
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'email', 'first_name', 'last_name'),
        }),
    )

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'avatar', 'bio', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__phone_number', 'user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at']
    fields = ['user', 'avatar', 'bio', 'created_at']
    list_per_page = 10
    list_max_show_all = 100
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj=None):
        return False
    def has_view_permission(self, request, obj=None):
        return True
admin.site.register(Profile, ProfileAdmin)
admin.site.register(User, UserAdmin)