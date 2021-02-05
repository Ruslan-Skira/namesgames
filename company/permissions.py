from rest_framework.permissions import BasePermission

from accounts.models import User
from company.models import Company


# Utility user/group checkers


class PermissionsMapMixin:
    permission_classes_map = {}

    def get_permissions(self):
        action = getattr(self, "action")
        perms = self.permission_classes_map.get(action)
        if perms is None:
            perms = super().get_permissions()
        return perms


class IsEmployee(BasePermission):
    """
    Permission check for user in Company
    """

    def has_permission(self, request, view):
        return bool(request.user) \
               and request.user.is_authenticated \
               or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj) and bool(request.user) \
               and request.user.is_authenticated \
               or request.user.is_superuser


class IsCompanyOwner(IsEmployee):
    """
    Company Owner can CRUD the Employees in his company.
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_company_owner

    def has_object_permission(self, request, view, obj):
        """
        permission to get object has only company owner or admin.
        """
        return (
                super().has_object_permission(request, view, obj)
                and request.user.is_company_owner
        )


class IsCompanyEmployeeOrAdmin(IsEmployee):
    """
    Permission class for only colleagues or superuser.
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj: Company or User):
        """
        Rewriting base class.
        """

        if isinstance(obj, User):
            return (
                    bool(request.user)
                    and request.user.is_authenticated
                    and (
                            request.user.company_id == obj.company_id
                            or request.user.is_superuser
                    )
            )
        elif isinstance(obj, Company):
            return (
                    bool(request.user)
                    and request.user.is_authenticated
                    and (request.user.company_id == obj.id or request.user.is_superuser)
            )
        else:
            raise Exception(
                f"Obj: {obj._meta.model_name}is not Company or Employee instance"
            )


class IsCompanyOwnerOrAdmin(IsCompanyOwner):
    """
    Only company Owner can update the Company
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view) or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        """
        permission to get object has only company owner or admin.
        """
        return super().has_object_permission(request, view, obj) and request.user.is_company_owner or request.user.is_superuser
