# Generated by Django 5.1.7 on 2025-04-01 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0012_auto_20250320_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('room_searcher', 'Room Searcher'), ('room_owner', 'Room Owner'), ('broker', 'Broker')], default='room_searcher', help_text='Select your role in the RoomMate platform.', max_length=20),
        ),
        migrations.AlterField(
            model_name='facility',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='roomimage',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='roomlisting',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
