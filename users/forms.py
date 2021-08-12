from django import forms
from django.contrib import messages
from django.db import models
from django.db.models import fields
from django.http import request
from .models import Account
from django.forms.widgets import PasswordInput

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class' : 'form-control',
    }))
    repeate_password = forms.CharField(widget=PasswordInput(attrs={
        'placeholder': 'Repeate Password',
        'class' : 'form-control',
    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'city']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['city'].widget.attrs['class'] = 'form-control'
        self.fields['phone_number'].widget.attrs['class'] = 'form-control'

    # def clean(self):
    #     cleaned_data = super(RegistrationForm, self).clean()
    #     password = cleaned_data.get('password')
    #     repeate_password = cleaned_data.get('repeate_password')

    #     if password != repeate_password:
    #         raise forms.ValidationError(
    #             "Password does not match!"
    #         )