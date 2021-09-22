from django import forms
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from company.models import Company


class CompanyEditForm(forms.ModelForm):
    """
    Additional form for company-owner during adding and editing Company model

    """

    company_owner = forms.EmailField()

    def save(self, commit=True):
        company_owner = self.cleaned_data.get("company_owner", None)

        if company_owner and self.instance:
            user_model = get_user_model()
            user_model.objects.create(email=company_owner, company_id=1)
            send_mail(
                "Subject here",
                "Here is the message.",
                "nina.agneshka@gmail.com",
                ["skira.ruslan@gmail.com"],
                fail_silently=False,
            )
        return super().save(commit=commit)

    class Meta:
        model = Company
        fields = "__all__"
