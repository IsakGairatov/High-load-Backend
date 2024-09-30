# Generated by Django 3.2.12 on 2024-09-29 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_api_1', '0004_tag_tagrelationship'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(through='blog_api_1.TagRelationship', to='blog_api_1.Tag'),
        ),
    ]