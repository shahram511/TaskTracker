from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings 
from datetime import timedelta
from django.utils import timezone
from .models import Task

print("celery is working")
@shared_task
def send_daily_reminders():

    #find tommorow's date
    tomorrow = timezone.now() + timedelta(days=1)

    #find all tasks that are due tomorrow and doesnt done yet
    pending_tasks = Task.objects.filter(due_date=tomorrow, status__in=['todo', 'in_progress'])

    email_count = 0
    
    #send email to each user who has pending_tasks
    for task in pending_tasks:
        user = task.owner
        if user.email:
            subject = f"Reminser:'{task.title}' is due tomorrow"
            message = (
                f"hello {user.first_name} {user.last_name} \n\n"
                f"this is the reminder that your task  '{task.title}'needs to be finished by tomorrow "
                f"Priority: {task.priority}\n\n"
                f"Good luck!"
            )
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            email_count +=1
    return f"Done! sent {email_count} reminder emails"        
    #tell celery when to run this task
