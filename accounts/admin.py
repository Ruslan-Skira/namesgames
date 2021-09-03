from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
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
    list_display = ('email', 'is_company_owner', 'password')
    list_filter = ('is_company_owner',)
    fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2', 'company', 'user_permissions', 'groups')}),
        ('Permissions', {'fields': ('is_superuser', 'is_company_owner', 'is_staff')}),
        ('Personal information', {
            'classes': ('collapse',),
            'fields': ('first_name', 'last_name', 'picture_url', 'position', 'birthday', 'phone_number', 'skype', 'deleted_at')
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
    # inlines = (UserProfileInline,)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj=None, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()

        if not is_superuser:
            disabled_fields |= {
                'email',
                'is_superuser',
                'is_company_owner'
                'user_permissions',
            }
        # Prevent non-superuser from editing their own permissions
        if (
                not is_superuser
                and obj is not None
                and obj == request.user
        ):
            disabled_fields |= {
                'is_staff',
                'is_superuser',
                'is_company_owner'
                'groups',
                'user_permissions',
            }
        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form

    class Meta:
        model = User
        fields=['__all__']


# Re-register UserAdmin
admin.site.register(User, UserAdmin)
# admin.site.unregister(Group)
