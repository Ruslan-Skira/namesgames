from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Contact


class RegistrationForm(forms.Form):
    total = forms.IntegerField(
        validators=[
            MinValueValidator(50),
            MaxValueValidator(500)
        ]
    )


class NewslettersForm(forms.ModelForm):
    """Newsletter form"""
    class Meta:
        model = Contact
        fields = '__all__'
