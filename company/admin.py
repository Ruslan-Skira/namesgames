from django.contrib import admin
from .models import Company


class CompanyAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = self.model.all_objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def delete_model(self, request, obj):
        obj.hard_delete()


admin.site.register(Company, CompanyAdmin)
