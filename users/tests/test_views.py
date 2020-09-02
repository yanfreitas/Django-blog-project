from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages


class RegisterView(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/register/')
        self.assertEquals(response.status_code, 200)

    def test_view_accessible_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_redirects_on_seccess(self):
        data = {'username': 'usertest',
                'email': 'test@gmail.com',
                'password1': 'tests321',
                'password2': 'tests321'
                }
        response = self.client.post(reverse('register'), data=data)
        message = [m.message for m in get_messages(response.wsgi_request)]
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')

        # testing success message
        self.assertEqual(len(message), 1)
        self.assertEqual(str(message[0]), f'Your account has been created! You are now able to log in!')


class ProfileView(TestCase):

    def setUp(self):
        # create users
        test_user = User.objects.create_user(username='user1', password='user1senha')
        test_user.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('profile'))
        self.assertEquals(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/profile/')

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='user1', password='user1senha')
        response = self.client.get('/profile/')
        self.assertEquals(response.status_code, 200)

    def test_view_accessible_by_name(self):
        login = self.client.login(username='user1', password='user1senha')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username='user1', password='user1senha')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_form_username_initially_set_to_expected_date(self):
        login = self.client.login(username='user1', password='user1senha')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

        expected_initial_username = User.objects.get(id=1).username
        response_name = response.context['form'].initial['username']
        self.assertEqual(response_name, expected_initial_username)

    def test_form_email_initially_set_to_expected_date(self):
        login = self.client.login(username='user1', password='user1senha')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

        expected_initial_email = User.objects.get(id=1).email
        response_email = response.context['form'].initial['email']
        self.assertEqual(response_email, expected_initial_email)

    def test_redirects_on_seccess(self):
        login = self.client.login(username='user1', password='user1senha')
        data = {'username': 'usertest',
                'email': 'test@gmail.com',
                }
        response = self.client.post(reverse('profile'), data=data)
        message = [m.message for m in get_messages(response.wsgi_request)]
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/profile/')

        # testing success message
        self.assertEqual(len(message), 1)
        self.assertEqual(str(message[0]), f'Your account has been updated! ')

