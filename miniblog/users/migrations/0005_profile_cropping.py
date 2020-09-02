# Generated by Django 3.1 on 2020-09-02 00:55

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200901_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cropping',
            field=image_cropping.fields.ImageRatioField('image', '300x300', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='cropping'),
        ),
    ]
