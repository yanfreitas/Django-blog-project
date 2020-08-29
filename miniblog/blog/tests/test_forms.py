from django.test import SimpleTestCase
from blog.forms import CreateComments


class CreateCommentsTest(SimpleTestCase):

    def test_description_label(self):
        form = CreateComments()
        self.assertTrue(form.fields['description'].label == '')

    def test_form_is_valid(self):
        form = CreateComments(data={'description': 'just a test'})
        self.assertTrue(form.is_valid())

    def test_form_is_invalid(self):
        form = CreateComments(data={'description': ''})
        self.assertFalse(form.is_valid())