# Generated by Django 3.1.1 on 2025-03-20 13:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0010_auto_20250320_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomlisting',
            name='contact_number',
            field=models.CharField(blank=True, help_text='Enter your contact number (e.g., +91 12345 67890) for users to reach you.', max_length=15, null=True, validators=[django.core.validators.RegexValidator(message='Enter a valid phone number (e.g., +91 12345 67890).', regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
