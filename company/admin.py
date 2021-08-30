from django.contrib import admin
from company.models import Company
from company.forms import CompanyForm


class CompanyAdmin(admin.ModelAdmin):
    # @admin.display(description='Company Owner')
    # def company_owner(self, obj):
    #     return obj.employees.get(is_company_owner=True)
    readonly_fields = ('employees_count', 'deleted_at')

    def get_queryset(self, request):
        qs = self.model.all_objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def delete_model(self, request, obj):
        obj.hard_delete()

    list_display = ['name', 'slug']

    # form = CompanyForm
    # fieldsets = (
    #     (None, {
    #         'fields': ('name', 'slug',),
    #     }),
    # )

    def get_form(self, request, obj=None, change=False, **kwargs):
        if request.user.is_superuser:
            kwargs['form'] = CompanyForm
        return super().get_form(request, obj, **kwargs)


admin.site.register(Company, CompanyAdmin)
