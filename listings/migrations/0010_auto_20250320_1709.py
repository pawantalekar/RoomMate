# Generated by Django 3.1.1 on 2025-03-20 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0009_auto_20250320_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomlisting',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='roomlisting',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
