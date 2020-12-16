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

class LoginForm(forms.Form):
    # http: // localhost: 8080 / accounts / linkedin_oauth2 / login / callback /?code = AQR_cWwGO3G-dECI7LtFDK49W9weZjomKBcb2GraKDiNjcRz4tNaOnZ0WkK8vqSAL8-O4Son_HMGMA9eof3ivglt3_1zBsl550YWMUvxHYy_PivdJ6Dlu80kJzqaxkEb9vO0DBCGctl5TPxUDKjOlmmjMIl0CRYbzQuVMeo4LB1JNp5FeJTBRIUQUWAWsQ & state = opTr60wPbc6c
    pass