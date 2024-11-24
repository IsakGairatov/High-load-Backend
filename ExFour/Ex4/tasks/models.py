from django.db import models

# Create your models here.
from django.db import models
from encrypted_model_fields.fields import EncryptedCharField, EncryptedTextField


class Email(models.Model):
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    body = EncryptedTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="Pending")  # Status field


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="Pending")