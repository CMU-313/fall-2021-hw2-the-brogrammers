# Generated by Django 2.2.23 on 2021-09-28 00:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0008_reviewform_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewform',
            name='documents',
        ),
    ]
