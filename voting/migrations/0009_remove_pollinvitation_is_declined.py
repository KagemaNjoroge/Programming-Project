# Generated by Django 5.0.6 on 2024-06-11 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0008_pollinvitation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pollinvitation',
            name='is_declined',
        ),
    ]
