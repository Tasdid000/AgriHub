# Generated by Django 4.2.7 on 2024-09-26 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_government_support'),
    ]

    operations = [
        migrations.AddField(
            model_name='government_support',
            name='Title',
            field=models.CharField(default='', max_length=2000),
        ),
    ]
