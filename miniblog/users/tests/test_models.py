from django.test import TestCase
from users.models import Profiles
from django.contrib.auth.models import User, Permission


class ProfileTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create an user
        test_user = User.objects.create_user(username='user1', password='user1senha')
        test_user.save()

    def test_user_label(self):
        prof = Profiles.objects.get(id=1)
        field_label = prof._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'user')

    def test_image_label(self):
        prof = Profiles.objects.get(id=1)
        field_label = prof._meta.get_field('image').verbose_name
        self.assertEquals(field_label, 'image')

    def test_object_name(self):
        prof = Profiles.objects.get(id=1)
        expected_name = f'{prof.user.username} Profile'
        self.assertEquals(expected_name, str(prof))

    def test_image_size(self):
        prof = Profiles.objects.get(id=1)
        expected_image_size = (300, 300)
        self.assertEquals(expected_image_size, (prof.image.height, prof.image.width))
