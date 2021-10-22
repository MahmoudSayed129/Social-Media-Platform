from django import forms
from django.forms import fields
from .models import Image, Posts


class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Image
        fields = ('title', 'image')

