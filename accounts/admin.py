from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from .models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hash format
        user = super().save(commit=False)
        user.set_password(self.clean_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on the user, but replaces the password field with admin's
    password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'email', 'password', 'date_joined', 'is_active', 'is_superuser', 'is_company_owner', 'is_staff',
            'deleted_at')

    def clean_password(self):
        # not in field because it does not have access to the initial value
        return self.initial["password"]


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    # inlines = (EmployeeInline,)
    list_display = ('email', 'is_company_owner', 'password')
    list_filter = ('is_company_owner',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'company')}),
        ('Permissions', {'fields': ('is_superuser', 'is_company_owner')}),
        ('Personal information', {
            'classes': ('collapse',),
            'fields': ('picture_url', 'position', 'birthday', 'phone_number', 'skype', 'deleted_at')
        }),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'company')
    ordering = ('company',)
    filter_horizontal = ()

    class Meta:
        model = User


# Re-register UserAdmin
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
