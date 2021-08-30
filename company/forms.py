from django import forms
from .models import Company
from django.contrib.auth import get_user_model


class CompanyForm(forms.ModelForm):
    """
    Additional form for company owner field during adding and editing Company model

    """
    company_owner = forms.EmailField()

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        company_owner = self.cleaned_data.get('company_owner', None)

        if company_owner and self.instance:
            user_model = get_user_model()
            user_model.objects.create(email=company_owner, company_id=1)
        return super().save(commit=commit)

    class Meta:
        model = Company
        fields = '__all__'
