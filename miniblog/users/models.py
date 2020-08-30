from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profiles(models.Model):
    """Model that represent the profile of an user"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        """String for representing the Model object name"""
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        """Function to resize the images uploaded"""
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
