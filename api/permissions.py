from rest_framework import permissions
from account.models import CompanyProfile, Profile
from item.models import Address, Order


class IsCompanyProfileOrSuperuser(permissions.BasePermission):
    message = "حساب شما هنوز تایید نشده است یا هنوز حساب شرکتی نساخته اید"

    def has_permission(self, request, view):
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
        try:
            CompanyProfile.objects.get(user=request.user)
        except CompanyProfile.DoesNotExist:
            return True
        else:
            return False


class NotAuthenticated(permissions.BasePermission):
    message = "ابتدا از حساب خود خارج شوید"

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return False
        return True


class ProfileUpdatePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False


class IsUserHasAddress(permissions.BasePermission):
    message = "آدرسی نساخته اید"

    def has_permission(self, request, view):
        address_list = Address.objects.filter(user=request.user)
        if not address_list.exists():
            return False
        return True


class BasketPermission(permissions.BasePermission):
    message = "سبد شما خالی است یاابتدا آدرسی را انتخاب نکرده اید"

    def has_object_permission(self, request, view, obj):
        try:
            Address.objects.get(user=request.user, this_address=True)
        except Address.DoesNotExist:
            return False
        try:
            Order.objects.get(user=request.user)
        except Order.DoesNotExist:
            return False
        return obj.items.all().exists()


class MyItemPermission(permissions.BasePermission):
    message = "محصولی نساخته اید"

    def has_permission(self, request, view):
        return view.get_queryset().exists()


class OwnerDeleteOrderItem(permissions.BasePermission):
    message = "مجوز ورود ندارید"

    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user


class OwnerUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class CompanyProfileUpdatePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            CompanyProfile.objects.get(user=request.user)
        except CompanyProfile.DoesNotExist:
            return False
        if obj.user == request.user:
            return True
        return False
