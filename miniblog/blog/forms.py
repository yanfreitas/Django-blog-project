from django import forms
from blog.models import Comment


class CreateComment(forms.ModelForm):
    """The form that allows the user to create a comment"""

    class Meta:
        model = Comment
        fields = ['description']
        labels = {'description': ''}
