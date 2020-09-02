from django.test import SimpleTestCase
from blog.forms import CreateComment


class CreateCommentsTest(SimpleTestCase):

    def test_description_label(self):
        form = CreateComment()
        self.assertTrue(form.fields['description'].label == '')

    def test_form_is_valid(self):
        form = CreateComment(data={'description': 'just a test'})
        self.assertTrue(form.is_valid())

    def test_form_is_invalid(self):
        form = CreateComment(data={'description': ''})
        self.assertFalse(form.is_valid())