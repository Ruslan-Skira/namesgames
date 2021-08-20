from django.contrib import admin
from .models import Company


class CompanyAdmin(admin.ModelAdmin):
    # TODO: write down right Company Owner.
    @admin.display(description='Company Owner')
    def company_owner(self, obj):
        return obj

    def get_queryset(self, request):
        qs = self.model.all_objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def delete_model(self, request, obj):
        obj.hard_delete()

    list_display = ['name', 'slug', 'company_owner', 'employees_count']


admin.site.register(Company, CompanyAdmin)
