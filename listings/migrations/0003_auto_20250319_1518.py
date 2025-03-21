# Generated by Django 3.1.1 on 2025-03-19 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomlisting',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='roomlisting',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='room_pics/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='roomlisting',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
