# Generated by Django 4.2.7 on 2024-09-25 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_appointment_time_slot_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='media/userimage/userimage.png', upload_to='media/userimage'),
        ),
    ]
