from rest_framework.permissions import BasePermission


# Utility user/group checkers

class PermissionsMapMixin:
    permission_classes_map = {}

    def get_permissions(self):
        action = getattr(self, 'action')
        perms = self.permission_classes_map.get(action)
        if perms is None:
            perms = super(PermissionsMapMixin, self).get_permissions()
        return perms


class IsCompanyOwnerOrAdmin(BasePermission):
    """
    Only company Owner can update the Company
    """

    def has_object_permission(self, request, view, obj):
        return (bool(request.user) and
                request.user.is_authenticated and
                request.user.is_company_owner and
                request.user.company_id == obj.id
                )


class IsCompanyEmployee(BasePermission):
    """
    Permission check for user in Company
    """

    def has_permission(self, request, view):
        company_name = view.kwargs['slug']
        return user_is_company_employee(request.user, company_name)


def user_is_company_employee(user, company_name):
    return (
            bool(user) and
            user.is_authenticated and
            user.company.slug == company_name or
            user.is_superuser
    )


def user_is_staff(user):
    return (
            bool(user) and
            user.is_authenticated and
            user.is_staff
    )
