from django.db import models

# Create your models here.

class KeyValue(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)