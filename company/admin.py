from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import User, Company

User = get_user_model()

class CompanyAdmin(admin.ModelAdmin):
    pass


class EmployeeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Company, CompanyAdmin)

admin.site.register(User, UserAdmin)
