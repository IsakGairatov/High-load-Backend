# Generated by Django 5.1.2 on 2024-10-20 01:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api1', '0007_product_api1_produc_categor_180a19_idx'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddIndex(
            model_name='adress',
            index=models.Index(fields=['user'], name='api1_adress_user_id_eed777_idx'),
        ),
        migrations.AddIndex(
            model_name='busketitems',
            index=models.Index(fields=['buyer'], name='api1_busket_buyer_i_5ae341_idx'),
        ),
        migrations.AddIndex(
            model_name='purchase',
            index=models.Index(fields=['buyer'], name='api1_purcha_buyer_i_36d12e_idx'),
        ),
    ]
