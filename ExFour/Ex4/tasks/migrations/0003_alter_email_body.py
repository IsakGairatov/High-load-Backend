# Generated by Django 5.1.3 on 2024-11-24 13:42

import encrypted_model_fields.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_email_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='body',
            field=encrypted_model_fields.fields.EncryptedTextField(),
        ),
    ]