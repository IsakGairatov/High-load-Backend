# Generated by Django 5.1.2 on 2024-10-19 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api1', '0003_remove_busketitems_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='busketitems',
            name='adress',
        ),
    ]
