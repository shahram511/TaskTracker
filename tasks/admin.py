
from django.contrib import admin
from .models import Task
# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    
    list_display = ('owner', 'category', 'title', 'description', 'status', 'priority', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    list_editable = ('status',)
 