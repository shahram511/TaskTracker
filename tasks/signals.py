from django.db.models.signals import post_save
from .models import Task
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=Task)
def send_task_email(sender, instance, created, **kwargs):
    """
    send email to the user when a task is created
    """
    user_email = instance.owner.email
    if not user_email:
        return f"User {instance.owner.username} has no email address"

    if created:
        subject = f"New Task Created: {instance.title}"
        message = (
            f"Hello {instance.owner.username},\n\n"
            f"A new task has been created for you"
            f"Task Title: {instance.title}\n"
            f"Status: {instance.status}\n"
            f"Priority: {instance.priority}\n"
            f"Description: {instance.description}\n"
        )    
        
    else:
        subject = f"Task Updated: {instance.title}"
        message = (
            f"Hello {instance.owner.first_name or 'User'},\n\n"
            f"Your task status or details have been updated.\n\n"
            f"Title: {instance.title}\n"
            f"Current Status: {instance.status}\n"
            f"Current Priority: {instance.priority}"
        )
        
    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email], fail_silently=False)
    
    except Exception as e:
        print(f"Error sending email to {user_email}: {e}")