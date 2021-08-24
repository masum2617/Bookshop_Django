from django import forms
from django.forms import fields, models
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['subject', 'review', 'rating']