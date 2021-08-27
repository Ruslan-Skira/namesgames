from django import forms
from .models import Company
from accounts.models import User


class CompanyForm(forms.ModelForm):
    """
    Additional form for company owner field during adding and editing Company model

    """
    company_owner = forms.ModelChoiceField(queryset=User.objects.all())

    def __init__(self, *args, **kwargs):
        companyid = kwargs.get('instance', None).id
        super().__init__(*args, **kwargs)

        if companyid:
            self.fields['company_owner'].queryset = User.objects.filter(company=companyid)

    def save(self, commit=True):
        company_owner = self.cleaned_data.get('company_owner', None)
        if company_owner:
            company_owner.is_company_owner = True
            company_owner.save()
        return super().save(commit=commit)

        # TODO: need to fix error here I do not understand how to do it.

        class Meta:
            model = Company
