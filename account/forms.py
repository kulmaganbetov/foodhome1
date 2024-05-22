from django import forms
from django.contrib.auth.models import User
from .models import UserSite


class UserRegistrationForm(forms.ModelForm):    
    password = forms.CharField(label='Введите пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)
    phone_number = forms.CharField(label='Введите whatsapp номер')

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data        
        if cd['password'] != cd['password2']:            
            raise forms.ValidationError('Passwords don\'t match.')        
        return cd['password2']


# Форма сайта пользователя
class UserSiteForm(forms.ModelForm):

    class Meta:
        model = UserSite
        fields = ('slug', 'phone_number')
        exclude = ('user', 'site')
