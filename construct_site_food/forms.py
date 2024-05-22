from string import Template
from django import forms
from django.forms import ImageField
from .models import Good


class GoodForm(forms.ModelForm):
    photo = ImageField(widget=forms.FileInput)

    class Meta:
        model = Good
        fields = (
            'title', 'price', 'old_price', 'photo',
            'category', 'description'
        )