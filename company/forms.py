from django import forms
from django.contrib.auth import get_user_model

from .models import Company


class CompanyAddForm(forms.ModelForm):
    """
    Additional form for company-owner during adding and editing Company model

    """
    company_owner = forms.EmailField()

    def save(self, commit=True):
        company_owner = self.cleaned_data.get('company_owner', None)

        if company_owner and self.instance:
            user_model = get_user_model()
            user_model.objects.create(email=company_owner, company_id=1)
        return super().save(commit=commit)

    class Meta:
        model = Company
        fields = '__all__'


class CompanyChangeForm(forms.ModelForm):
    """
    Сustrom model form editing Company model

    """

    company_owner = forms.CharField()


    class Meta:
        model = Company
        fields = '__all__'
