from rest_framework.permissions import BasePermission


class IsCompanyOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return True


class IsCompanyEmployee(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.company_employees.all()

