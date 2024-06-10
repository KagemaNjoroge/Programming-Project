# Generated by Django 5.0.6 on 2024-06-08 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(default='profile/default/avatar.png', upload_to='profile_images/'),
        ),
    ]
