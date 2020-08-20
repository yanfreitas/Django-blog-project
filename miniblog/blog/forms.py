from django import forms
from blog.models import Comments


class CreateComments(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateComments, self).__init__(*args, **kwargs)  # Call to ModelForm constructor
        self.fields['description'].widget.attrs['cols'] = 60
        self.fields['description'].widget.attrs['rows'] = 10

    class Meta:
        model = Comments
        fields = ['description']
        labels = {'description': ''}
