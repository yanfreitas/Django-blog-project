# Generated by Django 3.1 on 2020-09-02 01:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_profile_cropping'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='cropping',
        ),
    ]
