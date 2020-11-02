from django.contrib import admin
from .models import Company, Employee


class CompanyAdmin(admin.ModelAdmin):
    pass


class EmployeeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Company, CompanyAdmin)
admin.site.register(Employee, EmployeeAdmin)

