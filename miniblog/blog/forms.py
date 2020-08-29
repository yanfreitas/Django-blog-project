from django import forms
from blog.models import Comments


class CreateComments(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ['description']
        labels = {'description': ''}