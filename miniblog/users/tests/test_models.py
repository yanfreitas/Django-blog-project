from django.test import TestCase
from users.models import Profiles
from django.contrib.auth.models import User
from blog.tests.base_tests import test_model_fields_label


class ProfileTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create an user
        test_user = User.objects.create_user(username='user1', password='user1senha')
        test_user.save()

    def test_user_label(self):
        test_model_fields_label(self, Profiles, 'user', 'user')

    def test_image_label(self):
        test_model_fields_label(self, Profiles, 'image', 'image')

    def test_object_name(self):
        prof = Profiles.objects.get(id=1)
        expected_name = f'{prof.user.username} Profile'
        self.assertEquals(expected_name, str(prof))

    def test_image_size(self):
        prof = Profiles.objects.get(id=1)
        expected_image_size = (300, 300)
        self.assertEquals(expected_image_size, (prof.image.height, prof.image.width))
