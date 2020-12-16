from rest_framework.permissions import BasePermission


class isCompanyOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj, 'what is here??', obj.company_employees.all(), '++++++++++++++++++++++++++++++++++++++')
        return True

# TODO : rename
class isCompanyEmployee(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.company_employees.all()
    pass
