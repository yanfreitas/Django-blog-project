from django.test import TestCase
from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


class UserRegisterTest(TestCase):

    def test_email_label(self):
        form = UserRegisterForm()
        self.assertTrue(form.fields['email'].label is None or form.fields['email'].label == 'Email')

    def test_username_label(self):
        form = UserRegisterForm()
        self.assertTrue(form.fields['username'].label == 'Username')

    def test_password1_label(self):
        form = UserRegisterForm()
        self.assertTrue(form.fields['password1'].label == 'Password')

    def test_password2_label(self):
        form = UserRegisterForm()
        self.assertTrue(form.fields['password2'].label == 'Password confirmation')

    def test_form_is_valid(self):
        data = {'username': 'usertest',
                'email': 'test@gmail.com',
                'password1': 'tests321',
                'password2': 'tests321'
                }
        form = UserRegisterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_username_invalid(self):
        data = {'username': '',
                'email': 'test@gmail.com',
                'password1': 'tests321',
                'password2': 'tests321'
                }
        form = UserRegisterForm(data=data)
        self.assertFalse(form.is_valid())

    def test_form_email_invalid(self):
        data = {'username': 'testuser',
                'email': '',
                'password1': 'tests321',
                'password2': 'tests321'
                }
        form = UserRegisterForm(data=data)
        self.assertFalse(form.is_valid())

    def test_form_password_too_short(self):
        data = {'username': 'testuser',
                'email': 'test@gmail.com',
                'password1': 'test',
                'password2': 'test'
                }
        form = UserRegisterForm(data=data)
        self.assertFalse(form.is_valid())

    def test_form_different_passwords(self):
        data = {'username': 'usertest',
                'email': 'test@gmail.com',
                'password1': 'tests321',
                'password2': 'tests123'
                }
        form = UserRegisterForm(data=data)
        self.assertFalse(form.is_valid())


class UserUpdateTest(TestCase):

    def test_email_label(self):
        form = UserUpdateForm()
        self.assertTrue(form.fields['email'].label is None or form.fields['email'].label == 'Email')

    def test_username_label(self):
        form = UserUpdateForm()
        self.assertTrue(form.fields['username'].label == 'Username')

    def test_form_is_valid(self):
        data = {'username': 'usertest',
                'email': 'test@gmail.com',
                }
        form = UserUpdateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_username_invalid(self):
        data = {'username': '',
                'email': 'test@gmail.com',
                }
        form = UserUpdateForm(data=data)
        self.assertFalse(form.is_valid())

    def test_form_email_invalid(self):
        data = {'username': 'testuser',
                'email': '',
                }
        form = UserUpdateForm(data=data)
        self.assertFalse(form.is_valid())


class ProfileUpdateTest(TestCase):

    def test_image_label(self):
        form = ProfileUpdateForm()
        self.assertTrue(form.fields['image'].label == 'Image')
