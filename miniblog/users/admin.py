from django.contrib import admin
from .models import Profile
from image_cropping import ImageCroppingMixin


# Register the Profile model on the admin page
admin.site.register(Profile)
