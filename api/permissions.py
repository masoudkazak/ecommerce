from rest_framework import permissions
from account.models import CompanyProfile


class IsCompanyProfileOrSuperuser(permissions.BasePermission):
    message = "حساب شما هنوز تایید نشده است یا هنوز حساب شرکتی نساخته اید"

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
        return obj.company == request.user or request.user.is_superuser

# CP = CompanyProfile
class IsUserHasCPOrNot(permissions.BasePermission):
    message = "حساب شرکتی از قبل موجود است"

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            try:
                CompanyProfile.objects.get(user=request.user)
            except CompanyProfile.DoesNotExist:
                return True
            else:
                return False
