# Generated by Django 5.1.2 on 2024-10-20 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api1', '0006_adress_user'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['category'], name='api1_produc_categor_180a19_idx'),
        ),
    ]
