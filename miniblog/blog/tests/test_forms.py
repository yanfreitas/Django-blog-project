from django.test import SimpleTestCase
from blog.forms import CreateComments


class CreateCommentsTest(SimpleTestCase):

    def test_description_label(self):
        form = CreateComments()
        self.assertTrue(form.fields['description'].label == '')