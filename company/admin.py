from django.contrib import admin

from company.forms import CompanyAddForm, CompanyChangeForm
from company.models import Company


class CompanyAdmin(admin.ModelAdmin):
    """
        Admin site Company editing page
    """
    list_display = ['name', 'slug', 'company_owner']
    change_form_template = 'admin/change_company_form.html'

    def company_owner(self, instance) -> str:
        """
            method return company owner object.
        """
        try:
            company_owner_email = instance.employees.filter(
                is_company_owner=True).first().email  # TODO: in the future company owner should be one
        except Exception:
            company_owner_email = ''
        return company_owner_email

    def get_queryset(self, request):
        qs = self.model.all_objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def delete_model(self, request, obj):
        """
            methods delete model.
        """

        obj.hard_delete()

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = ('employees_count', 'deleted_at')
        self.form = CompanyAddForm
        return super().add_view(request, form_url='', extra_context=None)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.form = CompanyAddForm
        # self.form = CompanyChangeForm
        if not request.user.is_superuser:
            self.readonly_fields = ('name', 'slug', 'employees_count', 'deleted_at', 'company_owner')
        # self.list_display = ('name', 'slug', 'employees_count', 'deleted_at', 'company_owner')
        extra_context = extra_context or {}
        extra_context['company_owner'] = 'self.company_owner(object_id)'
        self.fields = ('name', 'slug', 'employees_count', 'deleted_at', 'company_owner')
        return super().change_view(request, object_id, form_url='', extra_context=extra_context)


admin.site.register(Company, CompanyAdmin)
