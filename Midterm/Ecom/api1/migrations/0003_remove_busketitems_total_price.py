# Generated by Django 5.1.2 on 2024-10-19 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api1', '0002_remove_busketitems_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='busketitems',
            name='total_price',
        ),
    ]
