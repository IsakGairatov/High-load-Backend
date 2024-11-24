from celery import shared_task
from django.core.mail import send_mail
from .models import *

@shared_task
def send_email_task(email_id):
    email = Email.objects.get(id=email_id)
    try:
        send_mail(email.subject, email.body, 'g_isakov@kbtu.kz', [email.recipient])
        email.status = "Sent"
    except Exception as e:
        email.status = "Failed"
    email.save()

@shared_task
def process_file_task(file_id):
    uploaded_file = UploadedFile.objects.get(id=file_id)
    try:
        # Process file securely
        uploaded_file.status = "Processed"
    except Exception:
        uploaded_file.status = "Failed"
    uploaded_file.save()