from rest_framework.permissions import BasePermission


# Utility user/group checkers


class IsCompanyOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return True


class IsCompanyEmployee(BasePermission):
    """
    Permission check for user in Company
    """
    def has_permission(self, request, view):
        company_name = view.kwargs['slug']
        return user_is_company_employee(request.user, company_name)


def user_is_company_employee(user, company_name):
    return(
        bool(user) and
        user.is_authenticated and
        user.company.slug == company_name or
        user.is_superuser
    )


def user_is_staff(user):
    return(
        bool(user) and
        user.is_authenticated and
        user.is_staff
    )