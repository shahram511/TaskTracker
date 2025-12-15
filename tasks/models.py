from enum import unique
from django.db import models
from users.models import User

# Create your models here.

class Tag(models.Model):
    name= models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

    
class Category(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['-created_at']


class Task(models.Model):
    choice_status = [
        ('todo', 'Todo'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]
    choice_priority = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    tags=models.ManyToManyField(Tag, blank=True, related_name='tasks')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_owner')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks_category')
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=choice_status, default='todo')
    priority = models.CharField(max_length=10, choices=choice_priority, default='low')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    
    
    

    