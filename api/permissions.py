from rest_framework import permissions
from account.models import CompanyProfile


class IsCompanyprofileOrSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            try:
                CompanyProfile.objects.get(user=request.user, confirm=True)
            except CompanyProfile.DoesNotExist:
                return False
            else:
                return True


class IsOwnerOrSuperuserOrReadonly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (obj.company == request.user
                or
                request.user.is_superuser
                )