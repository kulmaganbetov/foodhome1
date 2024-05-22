from django import forms
from django.contrib.auth.models import User
from .models import PhoneNumber, Support

# Форма номера телефона
class SupportForm(forms.ModelForm):

    class Meta:
        model = Support
        fields = ('label', 'whatsapp_text', 'bacground_color',
            'text_color', 'icon_color', 'kind')
        exclude = ('user_site',)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.slug = kwargs.pop('slug', None)
        print(self.slug)
        super().__init__(*args, **kwargs)


# Форма номера телефона
class PhoneNumberForm(forms.ModelForm):

    class Meta:
        model = PhoneNumber
        fields = ('phone_number',)
        exclude = ('support',)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

