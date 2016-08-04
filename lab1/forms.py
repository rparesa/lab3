from django import forms
from django.forms import ModelForm
from .models import URL

class URLForm(forms.ModelForm):

    class Meta:
        model = URL
        fields=('originalURL',)


