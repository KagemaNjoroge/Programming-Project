# Generated by Django 5.0.6 on 2024-06-11 09:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_alter_verificationcodes_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcodes',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 11, 9, 41, 19, 792514, tzinfo=datetime.timezone.utc)),
        ),
    ]
