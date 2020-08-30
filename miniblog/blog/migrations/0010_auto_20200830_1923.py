# Generated by Django 3.1 on 2020-08-30 22:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0009_post_likes'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Post',
            new_name='Posts',
        ),
        migrations.AlterField(
            model_name='comments',
            name='description',
            field=models.TextField(max_length=300),
        ),
    ]
