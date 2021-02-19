from rest_framework.permissions import BasePermission

from accounts.models import User
from company.models import Company


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
    Permission check is User Employee or not.
    """

    def has_permission(self, request, view):
        return bool(request.user) and request.user.is_authenticated and bool(request.user.company)

    def has_object_permission(self, request, view, obj: Company or User):
        """
        Rewriting base class.
        """
        is_authenticated = bool(request.user) and request.user.is_authenticated
        if isinstance(obj, User):
            return (
                    is_authenticated
                    and (
                            request.user.company_id == obj.company_id
                    )
            )
        elif isinstance(obj, Company):
            return (
                    is_authenticated
                    and request.user.company_id == obj.id
            )
        else:
            raise Exception(
                f"Obj: {obj._meta.model_name}is not Company or Employee instance"
            )


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
        return (super().has_permission(request, view) or request.user.is_superuser)

    def has_object_permission(self, request, view, obj: Company or User):
        """
        Employees or Superuser.
        """

        return (super().has_object_permission(request, view, obj) or request.user.is_superuser)


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
        return super().has_object_permission(request, view, obj) or request.user.is_superuser
