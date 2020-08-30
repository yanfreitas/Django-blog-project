from django import forms
from blog.models import Comments


class CreateComments(forms.ModelForm):
    """The form that allows the user to create a comment"""

    class Meta:
        model = Comments
        fields = ['description']
        labels = {'description': ''}