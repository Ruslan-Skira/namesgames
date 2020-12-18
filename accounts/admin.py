from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_company_owner')
    search_fields = ('email',)
    list_filter = ('is_company_owner',)


    class Meta:
        model = User


admin.site.register(User, UserAdmin)
